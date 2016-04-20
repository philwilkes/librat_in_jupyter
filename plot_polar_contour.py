# http://blog.rtwilson.com/producing-polar-contour-plots-with-matplotlib/

def plot_polar_contour(values, azimuths, zeniths):
    """Plot a polar contour plot, with 0 degrees at the North.
 
    Arguments:
 
     * `values` -- A list (or other iterable - eg. a NumPy array) of the values to plot on the
     contour plot (the `z` values)
     * `azimuths` -- A list of azimuths (in degrees)
     * `zeniths` -- A list of zeniths (that is, radii)
 
    The shapes of these lists are important, and are designed for a particular
    use case (but should be more generally useful). The values list should be `len(azimuths) * len(zeniths)`
    long with data for the first azimuth for all the zeniths, then the second azimuth for all the zeniths etc.
 
    This is designed to work nicely with data that is produced using a loop as follows:
 
    values = []
    for azimuth in azimuths:
      for zenith in zeniths:
        # Do something and get a result
        values.append(result)
 
    After that code the azimuths, zeniths and values lists will be ready to be passed into this function.
 
    """
 
    r, theta = np.meshgrid(zeniths, np.radians(azimuths))
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    plt.autumn()
    cax = ax.contourf(theta, r, values, 30)
    cb = fig.colorbar(cax)
    cb.set_label("Pixel reflectance")
 
    return fig, ax, cax
