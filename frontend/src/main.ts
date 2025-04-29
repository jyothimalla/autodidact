import { enableProdMode, importProvidersFrom } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { environment } from './environments/environment';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { ConfigService } from './app/services/config.service';
import { routes } from './app/app.routes';
import { provideRouter } from '@angular/router';

if (environment.production) {
  enableProdMode();
}

fetch('/assets/config.json')
  .then(response => response.json())
  .then(config => {
    const configService = new ConfigService({} as any); // we’ll override HttpClient later
    (configService as any).config = config;

    bootstrapApplication(AppComponent, {
      providers: [
        provideHttpClient(),
        provideRouter(routes),
        provideAnimations(),
        { provide: ConfigService, useValue: configService }
      ]
    });
  });
