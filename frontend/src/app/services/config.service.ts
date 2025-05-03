import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment} from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class ConfigService {
  apiBaseUrl: string = '';

  private config: { apiBaseUrl?: string } = {};

  constructor(private http: HttpClient) {}

  loadConfig(): Promise<void> {
    return fetch('/assets/config.json')
      .then(res => res.json())
      .then(config => {
        window.APP_CONFIG = config;
        this.apiBaseUrl = config.apiBaseUrl;
        console.log('✅ APP_CONFIG loaded:', config);
      })
      .catch(err => {
        console.warn('⚠️ Failed to load config.json, using fallback.');
        this.apiBaseUrl = environment.apiBaseUrl;
      });
  }
}
