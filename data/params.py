
#Samsung crop areas parameters
samsung_ecg_area = [0.035, 0.26, 0.945, 0.765]
samsung_ecg1_area = [0.035, 0.62, 0.945, 0.765]
samsung_ecg2_area = [0.2, 0.45, 0.8, 0.6]#[0.035, 0.45, 0.945, 0.6]
samsung_ecg3_area = [0.035, 0.28, 0.945, 0.43]

smsng_crop_areas = [samsung_ecg1_area, samsung_ecg2_area, samsung_ecg3_area]


#Apple crop areas parameters
#apple_ecg_area = [0.035, 0.26, 0.945, 0.765]
apple_ecg1_area = [0.05, 0.5, 0.95, 0.64]
apple_ecg2_area = [0.05, 0.35, 0.95, 0.45]
apple_ecg3_area = [0.05, 0.16, 0.95, 0.30]
apple_crop_areas = [apple_ecg1_area, apple_ecg2_area, apple_ecg3_area]
#Categories encoding
smote_class_dict = {
    0: 'AF',
    1: 'AFIB',
    2: 'AT',
    3: 'AVNRT',
    4: 'AVRT',
    5: 'SA',
    6: 'SAAWR',
    7: 'SB',
    8: 'SR',
    9: 'ST',
    10: 'SVT'
}

full_name_rythm = {
    'AF': 'Atrial Flutter',
    'AFIB': 'Atrial Fibrillation',
    'AT': 'Atrial Tachycardia',
    'AVNRT': 'Atrioventricular Nodal Reentrant Tachycardia',
    'AVRT': 'Atrioventricular Reentrant Tachycardia',
    'SA': 'Sinus Arrhythmia',
    'SAAWR': 'Sinus Atrium to Atrial Wandering Rhythm',
    'SB': 'Sinus Bradycardia',
    'SR': 'Sinus Rhythm',
    'ST': 'Sinus Tachycardia',
    'SVT': 'Supraventricular Tachycardia'
}
