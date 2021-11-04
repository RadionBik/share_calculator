import pandas as pd
import streamlit as st

MONEY_MEASURE = '[тыс. руб]'
START_SHARE = 0.5


class ShareCalculator:
    def __init__(self, p, remainder_share_percent):
        self.p = p
        self.remainder_share_percent = remainder_share_percent

    def calc_share_percent(self, profit_thousands) -> float:
        other_share = self.calc_other_share(profit_thousands)
        return other_share * 100 / profit_thousands

    def calc_other_share(self, profit, ) -> float:
        if profit <= self.p:
            return profit * START_SHARE
        else:
            return self.p * START_SHARE + (profit - self.p) * self.remainder_share_percent / 100

    def print_equation(self) -> str:
        return """
        Формула расчета:

        если ПРИБЫЛЬ <= П, то S = 50 [%] * ПРИБЫЛЬ,
        иначе S = {start_share} * {p} {money_measure} + (ПРИБЫЛЬ {money_measure} - {p} {money_measure}) * {share_percent}
        """.format(start_share=START_SHARE, p=self.p, share_percent=self.remainder_share_percent / 100,
                   money_measure=MONEY_MEASURE)


def main():
    st.markdown(
        """
        Формула расчета доли `S` задается двумя параметрами:
        * `П {money_measure}` - порог прибыли, для которого доля равна `50%`,
        * `R [%]` - процент на разницу между общей `ПРИБЫЛЬЮ` и `П`.

        """.format(money_measure=MONEY_MEASURE)
    )

    p = st.slider(f'Выбери П {MONEY_MEASURE}:', value=200, min_value=100, max_value=300)
    remainder_share_percent = st.slider(f'Выбери долю на остаток R [%]:', value=15, min_value=5, max_value=30)
    calculator = ShareCalculator(p, remainder_share_percent)
    st.text(calculator.print_equation())
    money_range = range(1, 500)
    st.line_chart(pd.DataFrame({
        'Доля S [%]': map(lambda x: calculator.calc_share_percent(x), money_range),
        f'Доля S {MONEY_MEASURE}': map(lambda x: calculator.calc_other_share(x), money_range),

    }))
    profit = st.number_input(f'Введи общую ПРИБЫЛЬ {MONEY_MEASURE}:', value=250.0)
    share_percent = calculator.calc_share_percent(profit)
    share = calculator.calc_other_share(profit)
    st.text('Для общей ПРИБЫЛИ = {} {money_measure}:\n'
            'S [%] = {:2.2f}\n'
            'S {money_measure} = ПРИБЫЛЬ {money_measure} * S [%] = {:4.2f}'.format(
        profit, share_percent, share, money_measure=MONEY_MEASURE
    ))


if __name__ == '__main__':
    main()
