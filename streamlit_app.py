import numpy as np
import pandas as pd
import streamlit as st

P1_SHARE = 50.0
P2_SHARE = 10.0


def solve_linear_equation(p1, p2):
    coeff_matrix = np.array([[1, p1], [1, p2]])
    dep_var = np.array([P1_SHARE, P2_SHARE])
    b, k = np.linalg.solve(coeff_matrix, dep_var)
    return k, b


class ShareCalculator:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        k, b = solve_linear_equation(p1, p2)
        self.k = k
        self.b = b

    def calc_share(self, profit_thousands) -> float:
        if profit_thousands <= self.p1:
            return P1_SHARE
        elif profit_thousands >= self.p2:
            return P2_SHARE
        else:
            return self.k * profit_thousands + self.b

    def print_equation(self) -> str:
        return """
        Формула расчета:
        
        если ПРИБЫЛЬ <= {}, то S={}
        если ПРИБЫЛЬ >= {}, то S={}
        иначе S={:2.4f} * ПРИБЫЛЬ + {:2.4f}
        """.format(self.p1, P1_SHARE, self.p2, P2_SHARE, self.k, self.b)


def main():
    st.markdown(
        """
        Формула доли S считается для диапазона `(П1, П2)`,
        где `П1` -- верхний порог прибыли, для которой доля `S=50%`,
        а `П2` -- нижний порог прибыли, для которой доля `S=10%`.
        
        Внутри диапазона используется линейное уравнение вида 
        `S = k * ПРИБЫЛЬ + b`, которое считается автоматически.
        """
    )
    p1 = st.slider('Выбери П1, тысяч рублей:', value=200, min_value=100, max_value=300)
    p2 = st.slider('Выбери П2, тысяч рублей:', value=500, min_value=200, max_value=800)
    calculator = ShareCalculator(p1, p2)
    st.text(calculator.print_equation())
    money_range = range(0, 1000)
    data = pd.DataFrame({
        'Доля S, %': map(lambda x: calculator.calc_share(x), money_range),
    })
    st.line_chart(data)
    profit = st.number_input('Введи общую прибыль, тысяч рублей:', value=250.0)
    share = calculator.calc_share(profit)
    st.text('Для общей прибыли в {} тыс. рублей S={:2.2f}%'.format(profit, share))


if __name__ == '__main__':
    main()
