import streamlit as st

allowed_emails = ["joaogpbdemelo@gmail.com","paloma3035.p@gmail.com"]

if not st.user.is_logged_in:
    st.login('google')
else:
    user_email = st.user.email

    if user_email in allowed_emails:
        st.write(f"Bem-vindo {st.user.name}!")  # <--- corrigido aqui
        # Conteúdo protegido
    else:
        st.warning("Você não tem permissão para acessar este app.")
        if st.button("Sair"):
            st.logout()
