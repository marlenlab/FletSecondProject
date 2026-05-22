import flet as ft
from db import main_db


def main_page(page: ft.Page):
    page.title = "ToDo List"
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    
    filter_type = {"value": "all"}

    
    def load_tasks():
        task_list.controls.clear()

        for task_id, task, completed in main_db.get_tasks(filter_type["value"]):
            task_list.controls.append(
                view_task(task_id, task, completed)
            )

        page.update()

   
    def toggle_task(task_id, is_completed):
        main_db.update_task(
            task_id=task_id,
            completed=int(is_completed)
        )
        load_tasks()

    def view_task(task_id, task_text, completed):
        task_field = ft.TextField(
            value=task_text,
            expand=True,
            read_only=True
        )

        def save_edit(e):
            main_db.update_task(
                task_id=task_id,
                new_task=task_field.value
            )
            task_field.read_only = True
            load_tasks()

        def toggle_edit(e):
            task_field.read_only = not task_field.read_only
            page.update()

        def del_button(e):
            main_db.delete_task(task_id=task_id)
            load_tasks()

        checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        edit_button = ft.IconButton(
            icon=ft.Icons.EDIT,
            on_click=toggle_edit
        )

        save_button = ft.IconButton(
            icon=ft.Icons.SAVE,
            on_click=save_edit
        )

        delete_button = ft.ElevatedButton('Delete', icon=ft.Icons.DELETE, color=ft.Colors.RED, on_click=del_button)

        return ft.Row([
            checkbox,
            task_field,
            edit_button,
            save_button,
            delete_button
        ])

    
    def add_task_flet(e):
        if task_input.value:
            task_text = task_input.value.strip()

            task_id = main_db.add_task(task_text)

            task_input.value = ""
            load_tasks()

    task_input = ft.TextField(
        label="Введите задачу",
        on_submit=add_task_flet
    )

    
    def set_filter(value):
        filter_type["value"] = value
        load_tasks()

    filter_buttons = ft.Row(
        [
            ft.ElevatedButton("Все задачи", on_click=lambda e: set_filter("all")),
            ft.ElevatedButton("В работе", on_click=lambda e: set_filter("uncompleted")),
            ft.ElevatedButton("Готово ✅", on_click=lambda e: set_filter("completed")),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )

    def del_completed_button(e):
        main_db.delete_completed_tasks()
        load_tasks()

    del_completed_btn = ft.ElevatedButton(
        "Очистить выполненные",
        color=ft.Colors.RED,
        on_click=del_completed_button
    )
   
    page.add(
        task_input,
        filter_buttons,
        del_completed_btn,
        task_list
    )

    load_tasks()


if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main_page)