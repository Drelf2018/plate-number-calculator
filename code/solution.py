"""
塔板数计算器
"""

from dataclasses import dataclass
from math import sqrt


@dataclass
class Solution:
    """
    解题方案

    beta (float): 回流比系数

    参考数据: 80, 0.65, 0.98, 0.02, 1.132, 1, 1.4
    """
    qnF: float
    xF: float
    xD: float
    xW: float
    alpha: float
    q: float
    beta: float

    def __post_init__(self):
        """
        物料衡算
        """
        self.qnD = self.qnF * (self.xF - self.xW) / (self.xD - self.xW)
        self.qnW = self.qnF - self.qnD
        self.get_R()
        self.get_plate_number()

    def get_xe(self) -> float:
        """
        计算 q 点坐标
        """
        if self.q == 1:
            self.xe = self.xF
        else:
            k = self.q / (self.q - 1)
            b = -self.xF / (self.q - 1)
            A = k * (self.alpha - 1)
            B = b * self.alpha - b - self.alpha + k
            self.xe = (-B - sqrt(B**2 - 4 * A * b)) / (2 * A)
        return self.xe

    def get_Rmin(self) -> float:
        """
        计算最小回流比
        """
        self.get_xe()
        self.ye = self.alpha * self.xe / (1 + (self.alpha - 1) * self.xe)
        self.Rmin = (self.xD - self.ye) / (self.ye - self.xe)
        return self.Rmin

    def get_R(self) -> float:
        """
        最小回流比乘以回流比系数得到实际回流比
        """
        self.get_Rmin()
        self.R = self.beta * self.Rmin
        return self.R

    def get_x(self, y: float) -> float:
        """
        相平衡方程
        """
        return y / (self.alpha - (self.alpha - 1) * y)

    def get_y_before(self, x: float) -> float:
        """
        精馏段方程
        """
        return (self.R * x + self.xD) / (self.R + 1)

    def get_y_after(self, x: float) -> float:
        """
        提馏段方程
        """
        return ((self.R * self.qnD + self.q * self.qnF) * x - self.qnW * self.xW) / (self.R * self.qnD + self.q * self.qnF - self.qnW)

    def get_plate_number(self):
        """
        迭代计算塔板数
        """
        self.x = [1]
        self.y = [1, self.xD]
        while self.x[-1] > self.xW:
            self.x.append(self.get_x(self.y[-1]))
            if self.x[-1] > self.xe:
                self.y.append(self.get_y_before(self.x[-1]))
            else:
                self.y.append(self.get_y_after(self.x[-1]))

    def result(self) -> list:
        return [
            f"{i}\t{round(self.x[i], 4)}\t{round(self.y[i], 4)}" for i in range(1, len(self.x))
        ]

    def export(self, file: str):
        """
        导出文件
        """
        self.get_plate_number()
        with open(file, "w", encoding="utf-8") as fp:
            fp.write("\n".join(self.result()))


if __name__ == "__main__":
    solution = Solution(80, 0.65, 0.98, 0.02, 1.132, 1, 1.4)
    solution.export("output.txt")