import pandas as pd
from app.config.settings import settings
from app.core.llm.llm_factory import LLMFactory
from app.core.agents.data_agent import DataAgent


if __name__ == "__main__":
    students_df = pd.read_csv('./data/Student Stress Monitoring Datasets/Stress_Dataset.csv')
    stress_mapping_df = pd.read_csv('./data/Student Stress Monitoring Datasets/StressLevelDataset.csv')

    llm_factory = LLMFactory()
    llm = llm_factory.get_llm(model=settings.MODEL_NAME, api_key=settings.LLM_API_KEY, temperature=0)

    agent = DataAgent(students_df, llm, stress_mapping_df)
    while True:
        query = input("User: ")
        query_result = agent.run(query)
        print("Agent Final Answer:", query_result['output'])
