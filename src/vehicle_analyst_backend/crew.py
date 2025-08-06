from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from src.vehicle_analyst_backend.tools.image_search_tool import ImageSearchTool

@CrewBase
class VehicleAnalystBackend():
    """VehicleAnalystBackend crew"""
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def vehicle_spec_comparer(self) -> Agent:
        return Agent(
            config=self.agents_config['vehicle_spec_comparer'],
            verbose=True
        )

    @agent
    def srilankan_ad_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['srilankan_ad_finder'],
            verbose=True
        )
    
    @agent
    def ad_report_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['ad_report_generator'],
            verbose=True
        )

    @task
    def spec_compare_task(self) -> Task:
        return Task(
            config=self.tasks_config['spec_compare_task'],
        )
    
    @task
    def vehicle_image_finder(self) -> Task:
        image_tool = ImageSearchTool()
        return Task(           
            config=self.tasks_config['vehicle_image_finder'],
            tools= [image_tool],
            verbose = True
        )
    
    @task
    def ads_for_vehicle1(self) -> Task:
        return Task(
            config=self.tasks_config['ads_for_vehicle1'],
        )
    
    @task
    def ads_for_vehicle2(self) -> Task:
        return Task(
            config=self.tasks_config['ads_for_vehicle2'],
        )
    
    @task
    def generate_ad_report(self) -> Task:
        return Task(
            config=self.tasks_config['generate_ad_report'],
        )
        
    @crew
    def vehicle_comparison_crew(self) -> Crew:
        return Crew(
            agents=[self.vehicle_spec_comparer()],
            tasks=[self.vehicle_image_finder(), self.spec_compare_task()],
            process=Process.sequential,
            verbose=True
        )
    
    @crew
    def ad_finder_crew(self) -> Crew:
        return Crew(
            agents=[self.srilankan_ad_finder(), self.ad_report_generator()],
            tasks=[self.ads_for_vehicle1(), self.ads_for_vehicle2(), self.generate_ad_report()],
            process=Process.sequential,
            verbose=True
        )