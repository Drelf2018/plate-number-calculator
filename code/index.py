import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from solution import Solution


app = FastAPI()


@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico")


@app.get("/")
async def _(qnF: float, xF: float, xD: float, xW: float, alpha: float, q: float, beta: float, r: int = 4):
    s = Solution(qnF, xF, xD, xW, alpha, q, beta)
    html = """<div style="margin: 0 auto;width: fit-content;"><title>塔板数计算器</title>
<strong>塔板数计算器</strong>
<span style="display:block;margin:1em 0">项目地址：<a href="https://github.com/Drelf2018/plate-number-calculator">https://github.com/Drelf2018/plate-number-calculator</a> .</span>
<span style="display:block;margin:1em 0">如有使用中的疑问、建议或问题反馈可在项目留言。</span></div>
<table frame="hsides" cellspacing="10" style="margin: 0 auto;text-align:center;">
    <tr>
        <th>塔板数(n)</th>
        <th>液相组成(xn)</th>
        <th>气相组成(yn)</th>
    </tr>
"""
    for i in range(1, len(s.x)):
        html += f"<tr><td>{i}</td><td>{round(s.x[i], r)}</td><td>{round(s.y[i], r)}</td></tr>"
    return HTMLResponse(html+"</table>")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)