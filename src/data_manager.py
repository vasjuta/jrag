import pandas as pd


class DataManager:
    def __init__(self, file_path):
        self.data = pd.read_excel(file_path)
        self.preprocess_data()

    def add_combined_text(self):
        self.data['combined_text'] = self.data.apply(lambda row: ' '.join([
            str(row['repository']), str(row['description']), str(row['remarks (internal)']),
            str(row['organization']), str(row['categories 1'])
            # , str(row['categories 2']), str(row['categories 3']), str(row['categories 4']),
            # str(row['technology'])
        ]), axis=1)
        self.data['combined_text'] = self.data['combined_text'].fillna('')

    def generate_docs(self, index_name):
        for _, row in self.data.iterrows():
            yield {
                "_index": index_name,
                "_source": row.to_dict()
            }

    def preprocess_data(self):
        self.add_combined_text()
        self.data.fillna('', inplace=True)

    def get_combined_data(self):
        return self.data[['combined_text']]

    def get_combined_texts(self):
        return self.data['combined_text'].tolist()

    def get_all_data(self):
        return self.data

    def get_data_by_query(self, query):
        # Simple query mechanism: filter by description and categories
        filtered_data = self.data[
            self.data.apply(lambda row: query.lower() in row['description'].lower() or
                                        query.lower() in row['categories 1'].lower() or
                                        query.lower() in row['categories 2'].lower() or
                                        query.lower() in row['categories 3'].lower() or
                                        query.lower() in row['categories 4'].lower(), axis=1)
        ]
        return filtered_data

    def get_summary_statistics(self):
        print("Summary Statistics:")
        print(f"Total number of datasets: {len(self.data)}")
        print("Datasets by organization:")
        print(self.data['organization'].value_counts())
        print("\nDatasets by organization type:")
        print(self.data['organization type'].value_counts())
        print("\nDatasets by category 1:")
        print(self.data['categories 1'].value_counts())

    def get_dataset_sizes_statistics(self):
        if 'size' in self.data.columns:
            print("Dataset Sizes Statistics:")
            print(self.data['size'].describe())
        else:
            print("No 'size' column found in the dataset.")

    def get_contact_information(self):
        contacts = self.data[['contact name', 'contact e-mail', 'organization']].drop_duplicates()
        print("Contact Information:")
        print(contacts)

    def print_eda(self):
        self.get_summary_statistics()
        self.get_dataset_sizes_statistics()
        self.get_contact_information()



