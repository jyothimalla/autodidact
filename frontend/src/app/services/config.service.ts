import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment} from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class ConfigService {
  apiBaseUrl: string = '';

  private config: { apiBaseUrl?: string } = {};

  constructor(private http: HttpClient) {}

  loadConfig(): Promise<void> {
    const isLocal =
      window.location.hostname === 'localhost' ||
      window.location.hostname === '127.0.0.1';
    const primaryConfigPath = isLocal ? '/assets/config.dev.json' : '/assets/config.prod.json';
    const fallbackConfigPath = '/assets/config.json';
    const defaultApiBaseUrl = isLocal ? 'http://localhost:8000' : 'https://api.autodidact.uk';

    return fetch(primaryConfigPath)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Failed to load ${primaryConfigPath}`);
        }
        return res.json();
      })
      .catch(() =>
        fetch(fallbackConfigPath).then((res) => {
          if (!res.ok) {
            throw new Error(`Failed to load ${fallbackConfigPath}`);
          }
          return res.json();
        })
      )
      .then((config) => {
        window.APP_CONFIG = config;
        this.apiBaseUrl = (config.apiBaseUrl || defaultApiBaseUrl).replace(/\/+$/, '');
        console.log('✅ APP_CONFIG loaded:', config);
      })
      .catch(() => {
        console.warn('⚠️ Failed to load runtime config, using default API URL.');
        this.apiBaseUrl = defaultApiBaseUrl || environment.apiBaseUrl;
        window.APP_CONFIG = { apiBaseUrl: this.apiBaseUrl };
      });
  }
}
