import flet as ft
from db import main_db


def main_page(page: ft.Page):
    page.title = 'Todo List'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column()

    def view_task(task_id , task_text):

        task_field = ft.TextField(value=task_text, expand=True, read_only=True)

        def save_edit(_):
            main_db.update_task(task_id=task_id, new_task = task_field.value)
            task_field.read_only = True
            page.update()

        
        def del_button(_):
            main_db.delete_task(task_id=task_id)
            task_list.controls.remove(task_row)
            page.update()


        delete_button = ft.ElevatedButton('Delete', icon=ft.Icons.DELETE, color=ft.Colors.RED, on_click=del_button)



        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_edit)


        def enable_edit(_):
            if task_field.read_only == True:
                task_field.read_only = False
            else:
                task_field.read_only = True
            page.update()

    

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)
        
        task_row = ft.Row([task_field,edit_button,save_button,delete_button])
        return task_row

    def add_task_flet(e):
        if text_input.value:
            task_text = text_input.value.strip()
            task_id = main_db.add(task=task_text)
            text_input.value = ""
            task_list.controls.append(view_task(task_id = task_id, task_text = task_text))
            page.update()

    text_input = ft.TextField(label='Введите задачу',on_submit=add_task_flet)

    page.add(text_input,task_list)


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main_page)

