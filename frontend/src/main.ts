import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { routes } from './app/app.routes';
import { ConfigService } from './app/services/config.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { appConfig } from './app/app.config';

const configService = new ConfigService();
configService.loadConfig().then(() => {
  // You can inject configService globally later if needed
  bootstrapApplication(AppComponent, appConfig)
    .catch(err => console.error('Bootstrap failed:', err));
});