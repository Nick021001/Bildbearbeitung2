# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 17:42:42 2024

@author: Daniel Salib, Niklas Rother
"""

import numpy as np
import skimage as ski
from skimage.exposure import adjust_log
import matplotlib.pyplot as plt
from scipy.fft import fft2, ifft2, fftshift, ifftshift

def hitp(u, v, k0):
    return np.where(np.sqrt(u**2 + v**2) <= k0, 1, 0)

def hihp(u, v, k0):
    return 1 - hitp(u, v, k0)

def hgtp(u, v, k0):
    return np.exp(-1 * ((np.sqrt(u**2 + v**2)**2) / (2 * k0**2)))

def hghp(u, v, k0):
    return 1 - hgtp(u, v, k0)

def apply_filter_gray(img, k0, filter_type="hghp"):
      # Iterate over color channels
    M, N = img.shape
    u, v = np.indices((M, N))
        
    centered_u = np.abs(u - (M / 2))
    centered_v = np.abs(v - (N / 2))
        
    fft_img = fft2(img)
    shifted_img = fftshift(fft_img)
        
    if filter_type == "hitp":
        filter_result = hitp(centered_u, centered_v, k0)
    elif filter_type == "hihp":
        filter_result = hihp(centered_u, centered_v, k0)
    elif filter_type == "hgtp":
        filter_result = hgtp(centered_u, centered_v, k0)
    elif filter_type == "hghp":
        filter_result = hghp(centered_u, centered_v, k0)
    else:
        raise ValueError("Invalid filter type")
            
    img_adp = shifted_img * filter_result
    
    unshifted_fft_result = fftshift(img_adp)
    inverse_fft_result = ifft2(unshifted_fft_result)
    
    return inverse_fft_result.real.astype(int)  

def apply_filter_rgb(img, k0, filter_type="hghp"):
    filtered_channels = []

    for channel in range(img.shape[-1]):  # Iterate over color channels
        filtered_channels.append(apply_filter_gray(img[:,:, channel], k0, filter_type=filter_type))

    # Combine the filtered channels back into an RGB image
    filtered_image = np.stack(filtered_channels, axis=-1)
    
    return filtered_image

def apply_filter(img, k0, filter_type="hghp"):
    if (len(img.shape) < 3):
        return apply_filter_gray(img, k0, filter_type = filter_type)
    else:
        return apply_filter_rgb(img, k0, filter_type = filter_type)
    
#image_cam = ski.data.camera()

#image = ski.data.astronaut()

#plt.set_cmap('gray')
#plt.imshow(apply_filter(image_cam, 32, "hghp"))
#plt.imshow(image[:, :, 0])
#plt.imshow(apply_filter_gray(image, 16, "hihp"))