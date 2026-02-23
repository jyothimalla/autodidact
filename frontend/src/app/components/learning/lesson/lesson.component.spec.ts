import { EMPTY } from 'rxjs';
import { LessonComponent } from './lesson.component';

describe('LessonComponent', () => {
  let component: LessonComponent;
  let routerMock: { navigate: jasmine.Spy };

  beforeEach(() => {
    routerMock = {
      navigate: jasmine.createSpy('navigate')
    };

    component = new LessonComponent(
      { paramMap: EMPTY } as any,
      routerMock as any,
      { back: jasmine.createSpy('back') } as any,
      { bypassSecurityTrustResourceUrl: (url: string) => url } as any,
      {} as any,
      { isAdmin: () => false } as any
    );
  });

  it('navigates to next level when available', () => {
    component.module = { id: 'python-programming' } as any;
    component.topic = {
      id: 'python-topic',
      name: 'Python',
      levels: [{ level: 1 }, { level: 2 }]
    } as any;
    component.currentLevel = { level: 1 } as any;

    component.completeLevel();

    expect(routerMock.navigate).toHaveBeenCalledWith([
      '/learning',
      'python-programming',
      'python-topic',
      'level',
      2
    ]);
  });

  it('alerts and returns to learning when no next level exists', () => {
    component.module = { id: 'python-programming' } as any;
    component.topic = {
      id: 'python-topic',
      name: 'Python',
      levels: [{ level: 1 }]
    } as any;
    component.currentLevel = { level: 1 } as any;

    const alertSpy = spyOn(window, 'alert');
    component.completeLevel();

    expect(alertSpy).toHaveBeenCalled();
    expect(routerMock.navigate).toHaveBeenCalledWith(['/learning']);
  });

  it('navigates to next atom for modules without nested topics', () => {
    component.module = {
      id: 'binary-number-system',
      atoms: [
        { id: 'binary-level-1', level: 1 },
        { id: 'binary-level-2', level: 2 }
      ]
    } as any;
    component.topic = undefined;
    component.currentLevel = { id: 'binary-level-1', level: 1 } as any;

    component.completeLevel();

    expect(routerMock.navigate).toHaveBeenCalledWith([
      '/learning',
      'binary-number-system',
      'binary-level-2'
    ]);
  });
});
