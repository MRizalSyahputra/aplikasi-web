import streamlit as st
import pandas as pd

st.title("Ini adalah halaman testing")

st.markdown("# Heading 1 pakai markdown")
st.markdown("## Heading 2 pakai markdown")
st.markdown("### Heading 3 pakai markdown")
st.markdown("**teks tebal**")
st.markdown("Nasi cumi hitam **Pak Kris** 50 ribu")
st.markdown("*teks miring*")
st.markdown("every *60 seconds*, a *minute* passed")
st.markdown("""
            > Ini adalah blockquote pertama.
            > 
            > > Ini adalah nested blockquote.
            > > 
            > > > Ini adalah nested blockquote di dalam blockquote kedua.
            > >
            > > Ini adalah nested blockquote.
            > 
            > Ini adalah blockquote pertama""")
st.markdown("""
            1. ordered list
            2. ordered list
            3. ordered list
            """)
st.markdown("""
            - unordered list
            - unordered list
            - unordered list
            """)
st.markdown("`System.out.println()`")
st.markdown("```java \n System.out.println()")
st.markdown("---")
st.header("beda header")
st.subheader("subheader dari beda header")
st.caption("bayangkan ada caption di sini")
st.text("ini adalah text gatau apa isinya 🗿")

