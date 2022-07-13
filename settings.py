SANTEC_SLM = False   # False for Hamamatsu SLM, True for Santec SLM

wavelength = 800e-9


if SANTEC_SLM:
    slm_size = (1200, 1920)
    chip_width = 15.36e-3
    chip_height = 9.6e-3
    bit_depth = 1023
else:
    slm_size = (600, 792)
    chip_width = 15.84e-3
    chip_height = 12e-3
    bit_depth = 255
