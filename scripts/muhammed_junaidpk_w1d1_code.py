import streamlit as st

st.title("Junaid")
 
st.header("About Me")
st.write("""
I'm Junaid, a BCA student from Kozhikode, Kerala.
I'm passionate about data analytics and enjoy working with data to find useful insights.
I'm currently building my skills through real-world project simulations and learning tools like Python and Excel.
""")

st.header("Skills")
st.markdown("""
- Python (pandas, matplotlib)
- Data Analysis
- Excel / Spreadsheets
- Report Generation (DOCX / PDF)
- Basic Web Development (HTML, CSS, JS)
- Data Visualization
""")

st.caption("muhammed junaid pk")
st.code("df=pd.read_csv('data/superstore.csv')", language="python")

st.latex(r'\text{profit margin} = \frac{\text{profit}}{\text{sales}}')
