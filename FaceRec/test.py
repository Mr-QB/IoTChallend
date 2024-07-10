class FaceDataLoader:
    def __init__(self, folder_data):
        self.folder_data = folder_data
        self.face_data = []
        self.embedding_extractor = EmbeddingExtractor()
        self.face_detector = FaceDetector()

    def loadFaceCroppedData(self):
        for label in os.listdir(self.folder_data):
            label_folder = os.path.join(self.folder_data, label)
            if os.path.isdir(label_folder):
                for filename in os.listdir(label_folder):
                    file_path = os.path.join(label_folder, filename)
                    if os.path.isfile(file_path):
                        image = cv2.imread(file_path)
                        if image is not None:
                            faces_cropped, x, y = self.face_detector.detect_face(image)
                            self.face_data.append(
                                {"label": label, "face": faces_cropped[0]}
                            )

        self.face_data_df = pd.DataFrame(self.face_data)
        return self.face_data_df

    def loadEmbeddingData(self):
        for label in os.listdir(self.folder_data):
            label_folder = os.path.join(self.folder_data, label)
            if os.path.isdir(label_folder):
                for filename in os.listdir(label_folder):
                    file_path = os.path.join(label_folder, filename)
                    if os.path.isfile(file_path):
                        image = cv2.imread(file_path)
                        if image is not None:
                            embedding = self.embedding_extractor.embedding(image)
                            if type(embedding) == np.ndarray:
                                self.face_data.append(
                                    {"label": label, "embedding": embedding}
                                )
                            else:
                                plt.imshow(image)

        self.face_data_df = pd.DataFrame(self.face_data)
        return self.face_data_df
