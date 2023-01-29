import dtlpy as dl

#My dataloop Credentilas
email='narsi.electrical999@gmail.com'
password = ''

def run_the_dataloop():
    #Login method
    if dl.token_expired():
        #dl.login()
        dl.login_m2m(email=email, password=password)
        # Get the project

    #project = dl.projects.create(project_name='Sports Events') #create your project

    project = dl.projects.get(project_name='Sports Events')
    # Get the dataset
    #dataset = project.datasets.get(dataset_name='My Fitst testing')
    # Get items in pages (100 item per page)

    #Creating a New DataSet
    data_set = project.datasets.create(dataset_name='My-Testing-Dataset')

    #gettign the created dataset
    dataset = project.datasets.get(dataset_name='My-Testing-Dataset')

    #creating the Labesl
    labels = [
        dl.Label(tag='Class1', color=(255, 100, 0)),
        dl.Label(tag='Class2', color=(34, 56, 7)),
        dl.Label(tag='key', color=(100, 14, 150))
    ]

    #labels = ['Class1', 'Class2', 'key']
    dataset.add_labels(label_list=labels)

    #Createting the Recipe with labels
    recipe = dataset.recipes.create(recipe_name='My-Testing-Recipe', labels=labels)

    #Uploading the Data
    dataset.items.upload(local_path='D:/Projects_DA/Testing') #Chnage your path here

    #Filtering the  uploaded items
    filters = dl.Filters()
    filters.add(field='dir', values='/Testing')

    item_list = dataset.items.list(filters=filters)

    #adding a labels to the Filetered items
    for items in item_list:
        for count, item in enumerate(items):
            if count < 2:
                builder = item.annotations.builder()
                builder.add(annotation_definition=dl.Classification(label='Class1'))
                item.annotations.upload(builder)
            else:
                builder = item.annotations.builder()
                builder.add(annotation_definition=dl.Classification(label='Class2'))
                item.annotations.upload(builder)

    # Filtering the Class1 labelled items
    class1_filter = dl.Filters(resource='annotations', field='label', values='Class1')

    item_Class1 = dataset.items.list(filters=class1_filter)
    # Count the items

    # Getting the All point Annotations Datasets
    annotations =  dataset.annotations.list()
    for annotation in annotations:
        annotation.print()


if __name__ == '__main__':
    run_the_dataloop()

