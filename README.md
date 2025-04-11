# Travel Planner Bot

Travel Planner Bot is a smart Streamlit application that helps you create customized, day-wise travel itineraries based on your preferences. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, this tool searches the web for relevant content and crafts a personalized itinerary that suits your interests, travel style, and daily pace.

## Folder Structure

```
Travel-Planner-Bot/
├── travel-planner-bot.py
├── README.md
└── requirements.txt
```

- **travel-planner-bot.py**: The main Streamlit application.
- **requirements.txt**: Required Python packages.
- **README.md**: This documentation file.

## Features

- **Travel Preferences Input:**  
  Provide your destination, travel dates, accommodation type, transport preference, interests, dietary needs, and pace.

- **AI-Powered Research:**  
  The Researcher agent generates a search query based on your preferences and finds the 10 most relevant travel articles using SerpAPI.

- **Day-wise Travel Itinerary:**  
  The Planner agent reads those links and creates a Markdown-formatted itinerary tailored to your selected destination, pace, and interests.

- **Smart Pacing:**  
  Activities per day are adjusted based on your selected itinerary pace (Relaxed, Balanced, or Active).

- **Markdown-Based Output:**  
  Your final itinerary is presented with clean Markdown styling and embedded hyperlinks for key places, restaurants, and experiences.

- **Download Option:**  
  Download the full itinerary as a `.txt` file for offline access or future reference.

- **Streamlined UI:**  
  Built with Streamlit for an intuitive and minimal user experience.

## Prerequisites

- Python 3.11 or higher
- An OpenAI API key (get one [here](https://platform.openai.com/account/api-keys))
- A SerpAPI key (get one [here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akash301191/Travel-Planner-Bot.git
   cd Travel-Planner-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:
   ```bash
   streamlit run travel-planner-bot.py
   ```

2. **In your browser**:
   - Provide your OpenAI and SerpAPI keys in the sidebar.
   - Fill out your travel details (destination, dates, preferences).
   - Click **🧭 Generate My Travel Itinerary**.
   - View and download your fully personalized Markdown-style itinerary.

3. **Download Option:**  
   Use the **📥 Download Itinerary** button to save your plan as a `.txt` file for offline use or sharing.

4. **Disclaimer:**  
   This itinerary is AI-generated using publicly available travel sources. Please verify activity availability, transportation schedules, and local restrictions before booking or traveling.

## Code Overview

- **`render_travel_inputs`**: Captures destination, preferences, dietary needs, and trip style.
- **`render_sidebar`**: Collects and stores OpenAI and SerpAPI keys securely in session state.
- **`generate_travel_itinerary`**: 
  - Calls the `Researcher` agent to perform a focused web search using SerpAPI.
  - Feeds the research results into the `Planner` agent to generate a detailed itinerary.
- **`main`**: Sets up page styling, orchestrates sidebar and inputs, and handles itinerary generation and display.

## Contributions

Contributions are welcome! Feel free to fork the repository, submit a pull request, or suggest improvements. Please follow the existing coding style and ensure your changes are well-documented.