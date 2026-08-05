
def mandelbrot(c, max_iter=100):
    """Calculate Mandelbrot set value for complex number c"""
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def render_mandelbrot(width=80, height=24, zoom=1, offset=0):
    """Render ASCII Mandelbrot set"""
    chars = "@%#*+=-:. "
    for y in range(height):
        row = ""
        for x in range(width):
            real = (x / width - 0.5) * 3.5 / zoom + offset
            imag = (y / height - 0.5) * 2.0 / zoom
            c = complex(real, imag)
            value = mandelbrot(c)
            row += chars[value % len(chars)]
        print(row)

if __name__ == "__main__":
    render_mandelbrot(zoom=1.5, offset=-0.5)
