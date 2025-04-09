import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ConfigService {
  private config: any;

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
