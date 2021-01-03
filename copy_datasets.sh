mkdir -p ../early-sexual-predator-detection-lab/datasets/{VTPAN,PANC}/

for dataset in PANC VTPAN; do
        for datasetType in train test; do
                echo "copying $dataset $datasetType"
                cp "$dataset/datapacks/datapack-$dataset-$datasetType.json" ../early-sexual-predator-detection-lab/datasets/$dataset/
                cp "$dataset/csv/$dataset-$datasetType.csv" ../early-sexual-predator-detection-lab/datasets/$dataset/
        done
done

