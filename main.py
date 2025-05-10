from agents.customer_agent import CustomerAgent
from agents.product_agent import ProductAgent
from agents.recommendation_agent import RecommendationAgent
from agents.memory_agent import MemoryAgent

def run_demo(customer_id='cust001'):
    memory = MemoryAgent()
    customer = CustomerAgent(customer_id, memory)
    product_agent = ProductAgent(memory)
    recommender = RecommendationAgent(memory)

    # Customer views some product
    customer.browse_product('prod001')

    # Get and log recommendations
    recommendations = recommender.recommend(customer_id)
    customer.receive_recommendations(recommendations)

if __name__ == "__main__":
    run_demo()
