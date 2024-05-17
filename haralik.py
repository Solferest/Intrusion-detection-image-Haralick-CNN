
import mahotas
import pandas as pd
import os


damaged_files = []

def compute_haralick_features(image_path):
    try:
        img = mahotas.imread(image_path, as_grey=True)
        textures = mahotas.features.haralick(img)
        textures_all_angles = mahotas.features.haralick(img, return_mean=True, ignore_zeros=False)
    
        angles = [0, 45, 90, 135, 'Mean']

        # Create a DataFrame to store Haralick features
        df = pd.DataFrame(textures, columns=['Angular_Second_Moment', 'Contrast', 'Correlation', 'Variance',
                                             'Inverse_Difference_Moment', 'Sum_Average', 'Sum_Variance', 'Sum_Entropy',
                                             'Entropy', 'Difference_Variance', 'Difference_Entropy', 'Info_Measure_1',
                                             'Info_Measure_2'])
    
        # Add angle column
        df['Angle'] = angles[:-1]
    
        # Append row for mean values
        mean_values = list(textures_all_angles) + ['Mean']
        df.loc[len(df)] = mean_values
    
        # Add filename column
        df['Filename'] = os.path.basename(image_path)
    
        return df
    except Exception as e:
        print(f"Поврежденный файл: {image_path}")
        print(e)
        damaged_files.append(image_path)


def compute_haralick_features_for_folder(input_folder, output_folder, file_num):
    # Get all pcap files
    pcap_files = os.listdir(input_folder)

    # Initialize empty DataFrames for each angle
    dfs = {angle: pd.DataFrame() for angle in [0, 45, 90, 135, 'Mean']}
    count=0
    # Compute Haralick features for each file and append to the corresponding DataFrame
    for pcap_file in pcap_files:
        input_path = os.path.join(input_folder, f'{pcap_file}')
        count+=1
        print(count)
        df = compute_haralick_features(input_path)
        
        for angle in [0, 45, 90, 135, 'Mean']:
            dfs[angle] = pd.concat([dfs[angle], df[df['Angle'] == angle]], ignore_index=True)

    # Save each DataFrame to a CSV file
    for angle, df in dfs.items():
        df.to_csv(os.path.join(output_folder, f'{file_num}_haralick_{angle}.csv'), index=False)

def rename_files(input_folder):
    files = os.listdir(input_folder)
    for file in files:
        old_name = os.path.join(input_folder, file)
        new_name = os.path.join(input_folder, file.replace('.pcap.png', '.png'))
        os.rename(old_name, new_name)




input_folder = 'D:/pcapTest/images/Attack2/13/ZigZag'
output_folder = 'D:/pcapTest/haralik/Atack2/ZigZag'
#rename_files(input_folder)
compute_haralick_features_for_folder(input_folder, output_folder, 13)
input_folder = 'D:/pcapTest/images/Attack2/13/Hilbert'
output_folder = 'D:/pcapTest/haralik/Atack2/Hilbert'
#rename_files(input_folder)
compute_haralick_features_for_folder(input_folder, output_folder, 13)
input_folder = 'D:/pcapTest/images/Attack2/13/Linear'
output_folder = 'D:/pcapTest/haralik/Atack2/Linear'
#rename_files(input_folder)
compute_haralick_features_for_folder(input_folder, output_folder, 13)
input_folder = 'D:/pcapTest/images/Attack2/13/Spiral'
output_folder = 'D:/pcapTest/haralik/Atack2/Spiral'
#rename_files(input_folder)
compute_haralick_features_for_folder(input_folder, output_folder, 13)

print("Поврежденные файлы:")
for file in damaged_files:
    print(file)