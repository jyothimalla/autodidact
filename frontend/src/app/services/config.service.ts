import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment
  
 } from '../../environments/environment';
@Injectable({
  providedIn: 'root',
})
export class ConfigService {
  private config: any;

  apiBaseUrl = environment.apiBaseUrl;  // 🛡️ VPS IP
  // apiBaseUrl = 'http://localhost:8000'; // FastAPI backend
  async loadConfig(): Promise<void> {
    const hostname = window.location.hostname;
    const isProd = !hostname.includes('localhost');
  
    const configPath = isProd
      ? '/assets/config.prod.json'
      : '/assets/config.dev.json';

  const response = await fetch(configPath);
  if (!response.ok) {
    throw new Error(`Failed to load ${configPath}`);
  }

  this.config = await response.json();
}

  get apiUrl(): string {
    return this.config?.apiUrl ?? '';
  }
}
