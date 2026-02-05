import spacy
# from spacy_streamlit import visualize_tokens
import streamlit as st

pos_colors = {
        "NOUN": "#85C1E9",  
        "VERB": "#82E0AA",  
        "ADJ":  "#F7DC6F", 
        "PROPN": "#D7BDE2",
        "NUM":  "#F1948A"
    }
default_color = "#5D6D7E"

@st.cache_resource
def load_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")
        return spacy.load("en_core_web_sm")
 
nlp = load_model() 
    
def tokenize_input(text:str):
    return nlp(text)
def custom_metric(label, value, color_hex="#333", bg_color="#f0f2f6"):
    html_code = f"""
    <div style="
        background-color: {bg_color};
        text-align: center;
        ">
        <div style="color: {color_hex}; font-size: 14px; margin-bottom: 5px;">{label}</div>
        <div style="color: {color_hex}; font-size: 28px; font-weight: bold;">{value}</div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)
def get_metrics(tokens):
    pos_count = {
        "NOUN": 0,  
        "VERB": 0,  
        "ADJ": 0, 
        "PROPN": 0,
        "NUM": 0,
        "OTHERS" :0
    }
    for token in tokens:
        if token.pos_ in  ["NOUN","VERB","ADJ","PROPN","NUM"]:
            pos_count[token.pos_]+=1
        else:
            pos_count['OTHERS']+=1
    return pos_count

def display_metrics(tokens):
    metrics = get_metrics(tokens)
    cols = st.columns(len(metrics)+1)
    with cols[0]:
        custom_metric(label="All Tokens", value = len(tokens), bg_color="", color_hex="#FFFFFF")

    for i, (label, value) in enumerate(metrics.items(),start=1):
        with cols[i]:
            custom_metric(label=label, value = value,bg_color="",color_hex=pos_colors.get(label, default_color))
       
def display_tokens(tokens):
    html_string = "<div style='line-height: 2.5;'>"
    
    for token in tokens:
        color = pos_colors.get(token.pos_,default_color)
            # if token.pos_ =='VERB':
        html_string+=f"""<span style='background-color: {color}; padding: 4px 6px; border-radius: 4px; margin-right: 4px; color: black; font-weight: bold;' title='{token.pos_}'>{token.text} {f"[{token.ent_type_ }]" if token.ent_type_ else ""}</span>"""
        
    html_string+="</div>"
    
    st.markdown(html_string, unsafe_allow_html = True)
def clear_input():
    st.session_state.user_input_textarea = ""
    
def run_app():
    default_text = """Apple's name was inspired by Steve Jobs' visit to an apple farm. He was on a fruitarian diet, and it didn't seem intimidating! Dr. Smith said, "N.L.P. is 100% fun. Visit us at https://spacy.io or email hello@example.com."""
    
    st.title("NLP Tokenizer & Entity Recognizer")
    st.markdown("""
    This app uses **spaCy** to analyze text structure. It highlights:
    * **Parts of Speech:** Grammatical role (Noun, Verb, Adjective, etc.)
    * **Named Entities:** Real-world objects (People, Organizations, Locations)
    """)
    
    input_text= st.text_area('Raw Input', placeholder="Type or paste text here to see token analysis...", height =200, key='user_input_textarea')
    button_cols = st.columns([1,1,5])
        
    if  button_cols[0].button("Tokenize"):
        tokens= tokenize_input(input_text)
        
    
        display_metrics(tokens)
        st.markdown("Result:")

        display_tokens(tokens)
        # st.text_area('Output', disabled = True, value=tokens)
    
    button_cols[1].button("Clear", on_click = clear_input)
   
    with st.sidebar:
        st.header("About")
        st.markdown("Made with ❤️ by **Alex Ababu**")
        st.markdown(
        "[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/alex-ababu/)")
        st.markdown("---")
        st.markdown("**Library:** [spaCy](https://spacy.io/)")
        st.markdown("**Model:** `en_core_web_sm`")
        st.markdown("---")
        st.info("💡 **Tip:** Try pasting a news article headline to see how it handles names and dates!")
        with st.expander("ℹ️ How to read the tags"):
            st.markdown("""
            * <span style='color: #85C1E9'><b>NOUN</b></span>: People, places, things.
            * <span style='color: #82E0AA'><b>VERB</b></span>: Actions or states of being.
            * <span style='color: #F7DC6F'><b>ADJ</b></span>: Describes a noun.
            * <span style='color: #D7BDE2'><b>PROPN</b></span>: Proper nouns (Specific names).
            * **[ORG], [PERSON]**: Named Entities detected by the model.
            """, unsafe_allow_html=True)
if __name__ == "__main__":
   run_app()
    