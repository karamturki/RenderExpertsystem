import streamlit as st
import pandas as pd

def calculate_scene_metrics(scene_df):
    scene_df['CV'] = (scene_df['Wpolygons'] + scene_df['Wvertex'] + scene_df['Wobject'] + scene_df['Wlight'] + scene_df['Wmaterials']) / 5
    total_frames = scene_df['frames'].sum()
    scene_df['FV'] = scene_df['frames'] / total_frames
    scene_df['ASS'] = scene_df['CV'] + scene_df['FV']
    scene_df['speed_rank'] = abs(scene_df['ASS'] * 10).astype(int)
    return scene_df

def calculate_ultimate_rank(scene_df):
    ultimate_rank = scene_df['speed_rank'].sum() / len(scene_df)
    return int(round(ultimate_rank))

def find_matching_gpu(gpu_df, ultimate_rank):
    matching_gpu = gpu_df[gpu_df['speed_rank'] == ultimate_rank]
    if not matching_gpu.empty:
        return matching_gpu.iloc[0]['GPU_model']
    else:
        return "No matching GPU found"

def main():
    st.title("GPU Scene Processor")

    st.header("Upload Scene File")
    scene_file = st.file_uploader("Upload the scene.xlsx file", type=["xlsx"])

    if scene_file:
        scene_df = pd.read_excel(scene_file)
        updated_scene_df = calculate_scene_metrics(scene_df)

        st.header("Processed Scene Data")
        st.write(updated_scene_df)

        ultimate_rank = calculate_ultimate_rank(updated_scene_df)
        st.write("Ultimate Rank: ", ultimate_rank)

        st.header("Upload GPU File")
        gpu_file = st.file_uploader("Upload the GPU.xlsx file", type=["xlsx"])

        if gpu_file:
            gpu_df = pd.read_excel(gpu_file)
            matching_gpu_model = find_matching_gpu(gpu_df, ultimate_rank)
            st.write("Matching GPU Model: ", matching_gpu_model)

if __name__ == "__main__":
    main()
