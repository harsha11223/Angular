import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  APIURL = 'http://localhost:8000/';
  tasks: any[] = [];
  newTask = '';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.getTasks();
  }

  getTasks(): void {
    this.http.get(this.APIURL + 'get_tasks').subscribe((res: any) => {
      this.tasks = res;
    });
  }

  addTask(): void {
    if (!this.newTask.trim()) return;

    const fd = new FormData();
    fd.append('task', this.newTask);

    this.http.post(this.APIURL + 'add_task', fd).subscribe(() => {
      this.newTask = '';
      this.getTasks();
    });
  }

  deleteTask(id: number): void {
    const fd = new FormData();
    fd.append('id', String(id));

    this.http.post(this.APIURL + 'delete_task', fd).subscribe(() => {
      this.getTasks();
    });
  }
}
