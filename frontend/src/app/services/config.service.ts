import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment
  
 } from '../../environments/environment';
@Injectable({
  providedIn: 'root',
})
export class ConfigService {
  private config: { apiBaseUrl?: string } = {};

  constructor(private http: HttpClient) {}
  /**
   * Loads the configuration from config.json.
   * @returns A promise that resolves when the configuration is loaded.
   */
  loadConfig(): Promise<void> {
    return this.http.get<any>('/assets/config.json')
      .toPromise()
      .then(data => {
        this.config = data;
      })
      .catch(error => {
        console.error('❌ Failed to load config.json:', error);
      });
  }

  get apiBaseUrl(): string {
    if (!this.config || !this.config.apiBaseUrl) {
      throw new Error('❌ Config not loaded yet or apiBaseUrl missing');
    }
    return this.config.apiBaseUrl;
  }

}
