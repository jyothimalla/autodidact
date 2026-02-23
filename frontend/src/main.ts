import { enableProdMode } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { environment } from './environments/environment';
import { provideHttpClient } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { ConfigService } from './app/services/config.service';
import { routes } from './app/app.routes';
import { provideRouter } from '@angular/router';
import { APP_INITIALIZER } from '@angular/core';


if (environment.production) {
  enableProdMode();
}

export function loadAppConfig(configService: ConfigService): () => Promise<void> {
  return () => configService.loadConfig();
}

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),
    provideHttpClient(),
    provideAnimations(),
    ConfigService,
    {
      provide: APP_INITIALIZER,
      useFactory: loadAppConfig,
      deps: [ConfigService],
      multi: true
    }
  ]
});
