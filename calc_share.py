import numpy as np
import pandas as pd
import streamlit as st


def calc_share(profit_thousands, p1, p2):
    p1_share = 50
    p2_share = 10
    if profit_thousands <= p1:
        return p1_share
    elif profit_thousands >= p2:
        return p2_share
    else:
        coeff_matrix = np.array([[1, p1], [1, p2]])
        dep_var = np.array([p1_share, p2_share])
        b, k = np.linalg.solve(coeff_matrix, dep_var)
        return k * profit_thousands + b


def main():
    st.markdown(
        """
        Формула доли S считается для диапазона (P1, P2),
        где P1 -- верхний порог прибыли, для которой доля `S=50%`,
        а P2 -- нижний порог прибыли, для которой доля `S=10%`.
        
        Внутри диапазона используется линейное уравнение вида 
        `S = k * прибыль + b`
        """
    )
    p1 = st.slider('введи P1', value=100, min_value=50, max_value=150)
    p2 = st.slider('введи P2', value=500, min_value=200, max_value=1000)

    money_range = range(0, 1000)
    data = pd.DataFrame({
        'Доля S, %': list(map(lambda x: calc_share(x, p1, p2), money_range)),
    })
    st.line_chart(data)


if __name__ == '__main__':
    main()
