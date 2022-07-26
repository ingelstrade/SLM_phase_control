from settings import slm_size, wavelength, chip_width, chip_height, pixel_size
import numpy as np
from matplotlib import pyplot as plt

focal_length = 150e-3

# coordinates in the SLM plane
x_slm = np.linspace(-chip_width/2, chip_width/2, slm_size[1])
y_slm = np.linspace(-chip_height/2, chip_height/2, slm_size[0])

# coordinates in the image plane
x_img = np.fft.fftshift(np.fft.fftfreq(slm_size[1], 
                                       pixel_size/(wavelength*focal_length)))
y_img = np.fft.fftshift(np.fft.fftfreq(slm_size[0], 
                                       pixel_size/(wavelength*focal_length)))

def GS_algorithm(hologram, iterations):
    
    # initial guess for the phase 
    phi = np.random.rand(*slm_size) * 2 * np.pi - np.pi
    
    for i in range(iterations):
    
        # restore SLM-plane intensity
        A = np.ones(slm_size)
        f_slm = A*np.exp(1j*phi)
        
        # propagate
        x = np.fft.fftshift(np.fft.fft2(f_slm))
        B = np.abs(x)
        theta = np.angle(x)
        
        # apply constraints
        B = hologram
        f_img = B*np.exp(1j*theta)
        
        # invert propagation
        y = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(f_img)))
        A = np.abs(y)
        phi = np.angle(y)
    
    return A, phi


def normalized(data):
    return data/np.max(data)


def gaussian(sigma, mu_x=slm_size[1]/2, mu_y=slm_size[0]/2):
    X = np.arange(slm_size[1])
    Y = np.arange(slm_size[0])
    x, y = np.meshgrid(X,Y)
    return np.exp(-1/2 * (((x-mu_x)**2+(y-mu_y)**2)/sigma**2))

def flat_top(r, dx=slm_size[1]/2, dy=slm_size[0]/2):
    X = np.arange(slm_size[1])
    Y = np.arange(slm_size[0])
    x, y = np.meshgrid(X,Y)
    return np.where((x-dx)**2+(y-dy)**2 < r**2, 1, 0)


if __name__ == '__main__':
    
    A = np.ones(slm_size)
    B, phi = GS_algorithm(flat_top(7), 15)
    f_slm = abs(A)*np.exp(1j*phi)
    
    fft = np.fft.fftshift(np.fft.fft2(f_slm))
    
    plt.imshow(phi, cmap='twilight', interpolation='None',
               extent=[x_slm[0]*1e3,x_slm[-1]*1e3,y_slm[0]*1e3,y_slm[-1]*1e3])
    plt.xlabel('[mm]')
    plt.ylabel('[mm]')
    plt.colorbar(label='phase [rad]')
    plt.show()
    
    plt.imshow(np.abs(fft), cmap='inferno',
               extent=[x_img[0]*1e3,x_img[-1]*1e3,y_img[0]*1e3,y_img[-1]*1e3])
    plt.xlabel('[mm]')
    plt.ylabel('[mm]')
    plt.colorbar()
    plt.show()
    