import streamlit as st
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
from agno.models.openai import OpenAIChat

from textwrap import dedent
    
def render_travel_inputs():
    st.markdown("---")
    # Three-column layout
    col1, col2, col3 = st.columns(3)

    # Column 1: Basic Trip Info
    with col1:
        st.subheader("🌍 Trip Info")
        destination = st.text_input("Destination*", placeholder="e.g., Japan")
        start_date = st.date_input("Start Date*", format="DD/MM/YYYY")
        end_date = st.date_input("End Date*", format="DD/MM/YYYY")
        travelers = st.number_input("Number of Travelers*", min_value=1, step=1)

    # Column 2: Preferences
    with col2:
        st.subheader("🏨 Preferences")
        accommodation = st.selectbox(
            "Accommodation Type (optional)", 
            ["No preference", "Hotel", "Hostel", "Resort", "Airbnb"]
        )
        transport = st.selectbox(
            "Transport Type*", 
            ["Public transport", "Rental car", "Taxi/Uber", "Walking", "No preference"], 
            index=4
        )
        budget = st.text_input("Budget (optional)", placeholder="e.g., $1000–$1500")
        pace = st.selectbox(
            "Itinerary Pace*", 
            ["Relaxed (1–2 activities/day)", "Balanced (3–4 activities/day)", "Active (full-day plans)"]
        )

    # Column 3: Interests & Notes
    with col3:
        st.subheader("🧭 Interests & Notes")
        trip_type = st.multiselect(
            "Interests*", 
            ["Adventure", "Culture", "Nature", "City life", "Food", "History", "Relaxation"]
        )
        dietary = st.text_input("Dietary Preferences (optional)", placeholder="e.g., Vegan, Gluten-free")
        notes = st.text_area("Special Requests (optional)", placeholder="e.g., Anniversary trip, avoid long walks")

    # User Requirements
    user_requirements = f"""
    **Trip Overview:**
    - Destination: {destination}
    - Dates: {start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}
    - Travelers: {int(travelers)}
    - Accommodation: {accommodation}
    - Budget: {budget if budget.strip() else 'Not specified'}

    **Preferences:**
    - Interests: {', '.join(trip_type) if trip_type else 'Not specified'}
    - Itinerary Pace: {pace}
    - Local Transport: {transport}
    - Dietary Needs: {dietary if dietary.strip() else 'None'}
    - Notes: {notes if notes.strip() else 'None'}
    """

    return user_requirements

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Get your key from [SerpAPI](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def generate_travel_itinerary(user_requirements: str) -> str:
    research_agent = Agent(
        name="Researcher",
        role="Finds travel activities and accommodations based on detailed itinerary preferences",
        model=OpenAIChat(id='gpt-4o', api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a world-class travel researcher. Given a detailed user itinerary summary,
            you must generate one clear and focused search term that best captures the user's travel intent.
            Then search the web using that term, analyze the results, and return the top 10 most relevant links.
        """),
        instructions=[
            "Use the user's travel requirements to understand their travel preferences, location, interests, and travel style.",
            "Generate exactly ONE concise, highly relevant search term (e.g., '4-day Tokyo itinerary for food lovers' or 'best relaxing beaches in Bali').",
            "Avoid using too many keywords in the search term—keep it short and focused so search results stay relevant.",
            "Use `search_google` with this single term.",
            "From the search results, analyze and extract the 10 most relevant URLs or summaries that best align with the user's preferences.",
            "Focus on relevance, clarity, and usability of results.",
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        add_datetime_to_instructions=True,
    ) 

    response = research_agent.run(user_requirements)
    research_results = response.content 

    planner_agent = Agent(
        name="Planner",
        role="Creates a personalized, day-wise itinerary using user requirements and web content from provided URLs.",
        model=OpenAIChat(id='o3-mini', api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a senior travel planner responsible for crafting a thoughtful and customized travel itinerary. 
            You are given:
            1. A structured summary of the user's travel preferences and trip overview
            2. A list of URLs pointing to trusted travel articles and itinerary resources

            Your job is to analyze the content from the URLs and extract useful suggestions that align with the user's goals.
            Then, create a practical, engaging, and well-paced day-by-day travel itinerary.
        """),
        instructions=[
            "Carefully analyze the user's structured requirements. Pay close attention to:",
            "- **Destination**: Ensure all activities are relevant to this place.",
            "- **Travel Dates**: Match the itinerary length to these dates.",
            "- **Number of Travelers**: Suggest group-friendly or couple-friendly options where applicable.",
            "- **Accommodation Preference**: Highlight suitable styles (e.g., Airbnb, hotel) from the source content.",
            "- **Budget**: Keep recommendations aligned with the given range.",
            "- **Interests**: Prioritize experiences matching the user's selected themes (e.g., food, nature, culture).",
            "- **Itinerary Pace**: Adjust the number and intensity of activities per day:",
            "   - Relaxed pace: 1–2 activities/day",
            "   - Balanced pace: 3–4 activities/day",
            "   - Active pace: 5–6 activities/day",
            "- **Local Transport**: Consider walkability, public transit, or driving for suggestions.",
            "- **Dietary Needs**: Include vegetarian or dietary-specific recommendations where applicable.",
            "- **Special Notes**: For honeymoons, birthdays, etc., personalize the experience with meaningful touches.",
            
            "Now read and analyze the content from each research URL provided in the research results.",
            "Use only the insights from those links to suggest real activities, restaurants, attractions, etc.",
            "Do not fabricate or invent content. Only use what is verifiably found in the sources.",
            "Design a clean, personalized day-by-day itinerary using Markdown formatting.",
            "Use `### Day X – Month Day: [Descriptive Title]` as the heading for each day (e.g., `### Day 1 – April 10: Arrival & Higashiyama Charm`).",
            "Below each heading, list the activities for that day using bullet points, based on the selected pace.",
            "Group experiences logically by location, interest, or time of day.",
            "Embed hyperlinks in relevant keywords using Markdown, e.g., [Fushimi Inari Shrine](https://wanderlog.com/list/itinerary/20/5-day-kyoto-itinerary). Do not paste raw URLs.",
            "Do not include any summary or introductory paragraph. Begin directly with the day-wise itinerary.",
            "Ensure the itinerary is useful, coherent, and enjoyable to follow."
        ],
        add_datetime_to_instructions=True
    )  

    planner_input = f"""
    User Requirements:
    {user_requirements}

    Research Results:
    {research_results}

    Use these details to draft an itinerary
    """

    response = planner_agent.run(planner_input)
    itinerary = response.content 

    return itinerary

def main() -> None:
    # Page config
    st.set_page_config(page_title="Travel Planner Bot", page_icon="🧳", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🧳 Travel Planner Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Travel Planner Bot — a smart Streamlit assistant that curates personalized travel itineraries based on your destination, interests, and preferences, making your journey smooth, exciting, and well-organized.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_requirements = render_travel_inputs()

    st.markdown("---")

    if st.button("🧭 Generate My Travel Itinerary"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        else:
            with st.spinner("Crafting your personalized travel itinerary..."):
                itinerary = generate_travel_itinerary(user_requirements=user_requirements)
                st.session_state.itinerary = itinerary

    if "itinerary" in st.session_state:
        st.markdown("## 🧳 Travel Itinerary")
        st.markdown(st.session_state.itinerary, unsafe_allow_html=True)

        st.download_button(
            label="📥 Download Itinerary",
            data=st.session_state.itinerary,
            file_name="travel_itinerary.txt",
            mime="text/plain"
        )

if __name__ == "__main__": 
    main()