import streamlit as st
import pandas as pd
st.title("Sistema de Padaria - Padaria suave sabor")
st.write("__________________________________________________________")
st.header("Faça o seu pedido")
st.subheader("Selecione os itens e veja o valor total")
st.write("__________________________________________________________")
cliente = st.text_input("Qual é o seu nome, por favor?")
if cliente:
    st.write(f"Olá, **{cliente}**! Seja muito bem-vindo(a).")
st.write("__________________________________________________________")
cardapio = {
    "Pão Francês": 1.00,
    "Pão de Queijo": 3.50,
    "Fatia de Bolo": 5.00,
    "Café Expresso": 4.00,
    "Suco de Laranja": 7.00,
    "Misto Quente": 8.50
}
df_cardapio = pd.DataFrame(list(cardapio.items()), columns=["Item", "Preço (R$)"])
st.write("### Nosso Cardápio:")
st.write(df_cardapio)
st.write("__________________________________________________________")
itens_selecionados = st.multiselect(
    "Escolha os itens que deseja comprar:",
    list(cardapio.keys())
)
st.write("__________________________________________________________")
col_info, col_resultado = st.columns([2, 1])
with col_info:
    st.write("### Resumo do Pedido")
    with st.form('calcular_pedido'):
        st.write("Confirme os itens selecionados e clique no botão abaixo para somar:")
        botao_somar = st.form_submit_button('Calcular Total')
total = 0.0
for item in itens_selecionados:
    total += cardapio[item]
if botao_somar:
    with col_resultado:
        st.write("### Total:")
        st.title(f"R$ {total:.2f}")
st.write("__________________________________________________________")
finalizar = st.button("Finalizar Compra")
if finalizar:
    if cliente:
        st.write(f"Obrigado pela compra, **{cliente}**! A Padaria suave sabor agradece!")
    else:
        st.warning("Por favor, preencha o campo de nome antes de finalizar sua compra.")