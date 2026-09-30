from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a:int, b:int)-> int:
    """add 2 number"""
    return a + b

@mcp.tool()
def multiply(a:int, b:int)->int:
    """multiply 2 numbers"""
    return a*b

#the transport "stdio" arrgument tells the server to use standard input/output(stdin/stdout) to receive and respond to tool function call

if __name__=="__main__":
    mcp.run(transport="stdio")