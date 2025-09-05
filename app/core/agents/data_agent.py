import pandas as pd
from enum import Enum
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from langchain.tools import tool, BaseTool
from langchain_litellm.chat_models import ChatLiteLLM
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.core.agents.tools import inspection_tools, transformation_tools


class DataFrameType(Enum):
    PRIMARY = 'primary'
    MAPPING = 'mapping'


class ToolResponse(BaseModel):
    execution_success: bool
    error_message: Optional[str] = None
    success_message: Optional[str] = None
    other_info: Optional[Any] = None


class DataAgent:
    """
    A base agent class for interacting with a pandas DataFrame using LangChain.

    This class provides a foundational structure with a language model, a set of tools,
    and a prompt template. It can be extended to create more specialized agents.
    """
    def __init__(self, df: pd.DataFrame, llm: ChatLiteLLM, mapping_df: Optional[pd.DataFrame] = None):
        """
        Initializes the base agent.

        Args:
            df (pd.DataFrame): The pandas DataFrame the agent will work with.
            llm (ChatLiteLLM): The language model to power the agent.
        """
        self.dfs = {
            DataFrameType.PRIMARY: df,
            DataFrameType.MAPPING: mapping_df,
        }
        self.llm = llm
        self.tools = self.get_tools()
        self.prompt = self.get_prompt()
        self.agent_executor = self.create_executor()
        self.chat_history = []

    def _get_df(self, df_type: DataFrameType) -> Optional[pd.DataFrame]:
        return self.dfs[df_type]

    def _set_df(self, df: pd.DataFrame, df_type: DataFrameType = DataFrameType.PRIMARY) -> None:
        self.dfs[df_type] = df

    def get_tools(self) -> List[BaseTool]:
        """
        Returns a list of tools available to the agent.

        This method should be overridden in subclasses to add more specific tools.
        """
        return [
            self.get_column_names,
            self.get_column_detailed_information,
            self.get_categorical_and_continuous_info,
            self.get_column_sample_values,
            self.rename_column,
            self.replace_value,
            self.add_new_column_from_math_operation
        ]

    def get_prompt(self) -> ChatPromptTemplate:
        """
        Returns the base prompt template for the agent.

        Subclasses can extend or modify this prompt to provide specific instructions.
        """
        system_message = (
            "You are an expert assistant for working with pandas DataFrames. "
            "Your goal is to help the user by providing information or performing operations "
            "on the provided DataFrame. Use the available tools to answer questions."
        )
        return ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

    def create_executor(self) -> AgentExecutor:
        """
        Creates the AgentExecutor instance.
        """
        agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def run(self, query: str) -> Dict[str, Any]:
        """
        Runs a query through the agent and returns the result.
        """
        result = self.agent_executor.invoke({"input": query, "chat_history": self.chat_history})
        self.chat_history.append(HumanMessage(content=query))
        self.chat_history.append(AIMessage(content=result['output']))
        return result

    @tool
    def get_column_names(self, df_type: DataFrameType = DataFrameType.PRIMARY) -> ToolResponse:
        """
        Retrieves the names of all columns in the DataFrame.
        The response includes a list of column names.
        This is useful for understanding the DataFrame's structure.
        """
        try:
            column_names = inspection_tools.get_column_names(self._get_df(df_type))
            return ToolResponse(
                execution_success=True,
                success_message="Column names retrieved successfully",
                other_info=column_names
            )
        except Exception as e:
            return ToolResponse(
                execution_success=False,
                error_message=str(e)
            )

    @tool
    def get_column_detailed_information(self, column_name: str, df_type: DataFrameType = DataFrameType.PRIMARY) -> ToolResponse:
        """
        Provides detailed information about a specific column.
        This includes unique values, their counts, and percentages.
        The response contains a detailed summary of the column's data.
        Args:
            column_name: The exact name of the column to analyze.
        """
        try:
            column_detailed_info = inspection_tools.get_column_detailed_information(self._get_df(df_type), column_name)
            return ToolResponse(
                execution_success=True,
                success_message="Unique values retrieved successfully",
                other_info=column_detailed_info
            )
        except Exception as e:
            return ToolResponse(
                execution_success=False,
                error_message=str(e)
            )

    @tool
    def get_categorical_and_continuous_info(self, df_type: DataFrameType = DataFrameType.PRIMARY) -> ToolResponse:
        """
        Classifies all columns in the DataFrame as either categorical or continuous.
        For categorical columns, it returns a list of their unique values.
        This tool is helpful for an initial assessment of the DataFrame's data types.
        """
        try:
            columns_info = inspection_tools.get_categorical_and_continuous_information(self._get_df(df_type))
            return ToolResponse(
                execution_success=True,
                success_message="Categorical and continuous info retrieved successfully",
                other_info=columns_info
            )
        except Exception as e:
            return ToolResponse(
                execution_success=False,
                error_message=str(e)
            )

    @tool
    def get_column_sample_values(self, num_samples: int = 5, df_type: DataFrameType = DataFrameType.PRIMARY) -> ToolResponse:
        """
        Retrieves sample of values from all columns.
        This tool is useful for quickly checking the pattern of values in all columns.
        Args:
                num_samples: The number of samples to retrieve.
            """
        try:
            sample_values = inspection_tools.get_column_sample_values(self._get_df(df_type), num_samples)
            return ToolResponse(
                execution_success=True,
                success_message="Sample values retrieved successfully",
                other_info=sample_values
            )
        except Exception as e:
            return ToolResponse(
                execution_success=False,
                error_message=str(e)
            )
        
    @tool
    def rename_column(self, old_column_name: str, new_column_name: str, df_type: DataFrameType = DataFrameType.PRIMARY) -> ToolResponse:
        """
        Renames a column in the DataFrame.
        
        Args:
            old_column_name: The current name of the column to be renamed.
            new_column_name: The new name for the column.
        """
        try:
            updated_df = transformation_tools.rename_column(self._get_df(df_type), old_column_name, new_column_name)
            self._set_df(updated_df, df_type)
            return ToolResponse(
                execution_success=True,
                success_message=f"Successfully renamed column '{old_column_name}' to '{new_column_name}'."
            )
        except Exception as e:
            return ToolResponse(
                execution_success=False,
                error_message=str(e)
            )

    @tool
    def replace_value(self, column_name: str, old_value: str, new_value: str, df_type: DataFrameType = DataFrameType.PRIMARY) -> ToolResponse:
        """
        Replaces a specific value in a column with a new value.
        
        Args:
            column_name: The name of the column where the replacement should occur.
            old_value: The value to be replaced.
            new_value: The new value to replace the old value.
        """
        try:
            updated_df = transformation_tools.replace_value(self._get_df(df_type), column_name, old_value, new_value)
            self._set_df(updated_df, df_type)
            return ToolResponse(
                execution_success=True,
                success_message=f"Successfully replaced '{old_value}' with '{new_value}' in column '{column_name}'."
            )
        except Exception as e:
            return ToolResponse(
                execution_success=False,
                error_message=str(e)
            )

    @tool
    def add_new_column_from_math_operation(self, column_name: str, operation_type: str, source_columns: List[str], df_type: DataFrameType = DataFrameType.PRIMARY) -> ToolResponse:
        """
        Adds a new column to the DataFrame by performing a safe, pre-defined operation on existing columns.
        
        This tool is designed to prevent unsafe code execution. It uses a controlled set of operations.

        Args:
            column_name (str): The name for the new column.
            operation_type (str): The type of operation to perform.
                - "sum": Adds the values of the source_columns.
                - "difference": Subtracts the second source_column from the first.
                - "product": Multiplies the values of the source_columns.
                - "quotient": Divides the first source_column by the second.
                - "mean": Calculates the average of the source_columns.
            source_columns (List[str]): A list of column names to use in the operation.
                - For "difference" and "quotient", the list must contain exactly two columns.
                - For other operations, the list can contain two or more columns.
        """
        try:
            updated_df = transformation_tools.add_new_column_from_math_operation(self._get_df(df_type), column_name, operation_type, source_columns)
            self._set_df(updated_df, df_type)
            return ToolResponse(
                execution_success=True,
                success_message=f"Successfully added new column '{column_name}' with a '{operation_type}' operation."
            )
        except Exception as e:
            return ToolResponse(
                execution_success=False,
                error_message=str(e)
            )
