import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { routes } from './app/app.routes';
import { ConfigService } from './app/services/config.service';

// ✅ Bootstrap using a wrapper to load config before launching app
bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(withFetch()),
    provideRouter(routes),
    ConfigService
  ]
}).then(appRef => {
  const injector = appRef.injector;
  const configService = injector.get(ConfigService);

  return configService.loadConfig();
}).catch(err => console.error('Bootstrap failed:', err));
