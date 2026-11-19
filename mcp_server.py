"""Part 2: the same tool on the sheet's side, as an MCP server.  Run: python mcp_server.py
The steps are in README.md."""
import csv, io, socket
from typing import Annotated
import requests
from fastmcp import FastMCP

SHEET = "https://docs.google.com/spreadsheets/d/1Kg6T-dJWaYx_JCPiRk3u0nBuAQcsCVRDPj1NFKP4WzM/gviz/tq?tqx=out:csv&headers=0&gid=368290478"

mcp = FastMCP("100x curriculum")

# Step 1. Move get_lecture here from tool_call.py and put @mcp.tool on the line above it.
# @mcp.tool
# def get_lecture(number):
#     for row in csv.reader(io.StringIO(requests.get(SHEET).text)):
#         if row[1].startswith(f"{number}. "):
#             return {"date": row[0], "title": row[1], "type": row[2], "tools": row[3]}
#     return {"error": f"There is no lecture {number}. Lectures run from 1 to 19."}

# Step 2. Write the card into the function itself: a docstring and a type hint.
@mcp.tool
def get_lecture(number: Annotated[int, "The lecture number, from 1 to 19."])-> dict:
    """
    Look up one lecture of the 100xEngineers Cohort 8 course by its number. 
    Returns that lecture's date, title, session type and the tools it covers. 
    Use it ONLY when the question is about a 100xEngineers Cohort 8 lecture. 
    Do NOT use it for any other course, school or program (for example Harvard CS50, Coursera, or a university class), 
    even if the question mentions a lecture number; answer those from your own knowledge instead.
    """
    for row in csv.reader(io.StringIO(requests.get(SHEET).text)):
        if row[1].startswith(f"{number}. "):
            return {"date": row[0], "title": row[1], "type": row[2], "tools": row[3]}
    return {"error": f"There is no lecture {number}. Lectures run from 1 to 19."}

# Any app can now reach it at http://localhost:8000/mcp
if __name__ == "__main__":
    if socket.socket().connect_ex(("127.0.0.1", 8000)) == 0:
        raise SystemExit("Port 8000 is already in use, probably by a server you started earlier. "
                         "Stop it with Ctrl+C in its terminal, or run: kill $(lsof -t -i:8000)")
    mcp.run(transport="http", port=8000)
