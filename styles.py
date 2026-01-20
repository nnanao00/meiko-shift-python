def get_mobile_css():
    return """
    <style>
        /* Desktop/Global Reset */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { margin-top: -30px; }
        
        /* Typography */
        html, body, [class*="css"]  {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-size: 14px; /* Standard desktop size */
        }
        
        /* Button Optimization */
        .stButton button {
            width: 100%;
            height: auto;
            min-height: 2.5rem;
            border-radius: 6px;
            font-weight: 600;
            margin-bottom: 0.2rem;
        }
        
        /* Calendar Day Cell */
        div[data-testid="column"] button {
             width: 100%;
             padding: 0.2rem 0.5rem;
             min-height: 80px !important; /* Proper height for Date + Shift text */
             height: auto;
             vertical-align: top; 
             line-height: 1.4; /* Better spacing for text */
             background-color: transparent;
             border: 1px solid #444; 
             text-align: left;
             font-size: 1.1rem;
             color: #ddd;
             display: block;
             white-space: pre-wrap; /* Ensure newlines render */
        }
        
        div[data-testid="column"] button:hover {
             border-color: #777;
             background-color: rgba(255,255,255,0.05);
        }

        /* Highlight selected day button */
        div[data-testid="column"] button[kind="primary"] {
            color: #ff4b4b; /* Highlight date text */
            font-weight: bold;
            background-color: rgba(255, 75, 75, 0.1);
        }

        /* Utility */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1200px; /* Constrain on ultra-wide screens */
        }
        
        hr { margin: 1em 0; }
        
    </style>
    """
