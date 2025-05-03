import { enableProdMode, importProvidersFrom } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { environment } from './environments/environment';
import { provideHttpClient, withInterceptors , HttpClient} from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { ConfigService } from './app/services/config.service';
import { routes } from './app/app.routes';
import { provideRouter } from '@angular/router';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { inject } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { APP_INITIALIZER } from '@angular/core';


if (environment.production) {
  enableProdMode();
}

export function loadAppConfig(configService: ConfigService): () => Promise<void> {
  return () => configService.loadConfig();
}

bootstrapApplication(AppComponent, {
  providers: [ provideRouter(routes),

    provideHttpClient(),
    ConfigService,
    {
      provide: APP_INITIALIZER,
      useFactory: loadAppConfig,
      deps: [ConfigService],
      multi: true
    }
  ]
});