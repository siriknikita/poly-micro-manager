# Архітектура проекту Poly Micro Manager

## Огляд архітектури

Poly Micro Manager представляє собою комплексну систему, що складається з трьох основних компонентів:

1. **Poly Micro Backend** - серверна частина на FastAPI з MongoDB
2. **Poly Micro Frontend** - клієнтська частина на React
3. **Tauri інтеграція** - об'єднує backend і frontend в десктопний додаток

Архітектура проекту побудована за принципами мікросервісної організації з чітким розділенням відповідальностей між компонентами.

## Backend архітектура

Backend Poly Micro Manager реалізує **Layered Microservices Architecture** з чітким розділенням обов'язків:

### Архітектурні шари

1. **API Layer**: Обробляє HTTP-запити, відповіді та маршрутизацію
2. **Service Layer**: Містить бізнес-логіку та оркеструє операції
3. **Repository Layer**: Керує доступом до даних та їх збереженням
4. **Schema Layer**: Визначає структури даних та валідацію
5. **Core Layer**: Містить конфігурацію та спільні утиліти

### Діаграма залежностей репозиторіїв

```mermaid
graph TD
    DB[Database] --> PR[ProjectRepository]
    DB --> SR[ServiceRepository]
    DB --> LR[LogRepository]
    DB --> MR[MetricsRepository]
    DB --> LCR[LogsCollectionRepository]
    
    subgraph Database Layer
        DB
    end
    
    subgraph Repository Layer
        PR
        SR
        LR
        MR
        LCR
    end
    
    classDef database fill:#e6ccff,stroke:#333,stroke-width:2px
    classDef repository fill:#d1e0ff,stroke:#333,stroke-width:1px
    
    class DB database
    class PR,SR,LR,MR,LCR repository
```

### Діаграма залежностей сервісів

```mermaid
graph TD
    %% Repository dependencies
    PR[ProjectRepository] --> PS[ProjectService]
    PR --> SS[ServiceService]
    PR --> MS[MetricsService]
    
    SR[ServiceRepository] --> SS
    SR --> MS
    
    LR[LogRepository] --> LS[LogService]
    
    MR[MetricsRepository] --> MS
    
    LCR[LogsCollectionRepository] --> SLS[ServiceLogsService]
    
    %% Service dependencies
    LS --> TS[TestService]
    
    subgraph Repository Layer
        PR
        SR
        LR
        MR
        LCR
    end
    
    subgraph Service Layer
        PS
        SS
        LS
        MS
        SLS
        TS
    end
    
    classDef repository fill:#d1e0ff,stroke:#333,stroke-width:1px
    classDef service fill:#d1f0d1,stroke:#333,stroke-width:1px
    
    class PR,SR,LR,MR,LCR repository
    class PS,SS,LS,MS,SLS,TS service
```

### Повна діаграма залежностей

```mermaid
graph TD
    %% Database
    DB[Database] --> PR
    DB --> SR
    DB --> LR
    DB --> MR
    DB --> LCR
    
    %% Repositories
    PR[ProjectRepository] --> PS[ProjectService]
    PR --> SS[ServiceService]
    PR --> MS[MetricsService]
    
    SR[ServiceRepository] --> SS
    SR --> MS
    
    LR[LogRepository] --> LS[LogService]
    
    MR[MetricsRepository] --> MS
    
    LCR[LogsCollectionRepository] --> SLS[ServiceLogsService]
    
    %% Services
    LS --> TS[TestService]
    
    %% API Routes (implied)
    PS --> API[API Endpoints]
    SS --> API
    LS --> API
    MS --> API
    SLS --> API
    TS --> API
    
    subgraph Data Layer
        DB
    end
    
    subgraph Repository Layer
        PR
        SR
        LR
        MR
        LCR
    end
    
    subgraph Service Layer
        PS
        SS
        LS
        MS
        SLS
        TS
    end
    
    subgraph API Layer
        API
    end
    
    classDef database fill:#e6ccff,stroke:#333,stroke-width:2px
    classDef repository fill:#d1e0ff,stroke:#333,stroke-width:1px
    classDef service fill:#d1f0d1,stroke:#333,stroke-width:1px
    classDef api fill:#ffe6cc,stroke:#333,stroke-width:1px
    
    class DB database
    class PR,SR,LR,MR,LCR repository
    class PS,SS,LS,MS,SLS,TS service
    class API api
```

## Frontend архітектура

Frontend Poly Micro Manager побудований на React з використанням сучасних патернів проектування:

### Структура компонентів

Frontend організований за принципом feature-based організації:

```
components/
├── auth/             # Функціонал аутентифікації
├── monitoring/       # Функціонал моніторингу
├── pipelining/       # CI/CD pipeline функціонал
├── testing/          # Функціонал автоматизованого тестування
└── shared/           # Спільні компоненти
```

### Патерни проектування

- **SOLID principles**: Адаптація SOLID принципів для React
- **Custom Hooks Pattern**: Відокремлення логіки від UI компонентів
- **Context API**: Глобальний стан додатку
- **Atomic Design**: Компоненти організовані за принципами атомарного дизайну

### Діаграма потоку користувача для моніторингу

```mermaid
sequenceDiagram
    title Metrics Exploration Flow

    actor User
    participant ServiceDetails
    participant Metrics

    User->>ServiceDetails: Click on metrics tab
    ServiceDetails->>Metrics: Request service metrics
    Metrics-->>User: Display performance graphs
    User->>Metrics: Adjust time range
    Metrics-->>User: Update metrics visualization
```

### Діаграма аутентифікації користувача

```mermaid
stateDiagram-v2
    [*] --> Unauthenticated

    state Unauthenticated {
        [*] --> LoginPage
        LoginPage --> AttemptLogin: Submit credentials
        AttemptLogin --> LoginFailed: Invalid credentials
        AttemptLogin --> LoginSuccessful: Valid credentials
        LoginFailed --> LoginPage: Try again
        LoginPage --> RegistrationPage: Register link
        RegistrationPage --> AttemptRegistration: Submit registration
        AttemptRegistration --> RegistrationFailed: Invalid information
        AttemptRegistration --> RegistrationSuccessful: Valid information
        RegistrationFailed --> RegistrationPage: Try again
        RegistrationSuccessful --> LoginPage: Redirect to login
    }
```

### Діаграма процесу тестування мікросервісів

```mermaid
flowchart TD
    A[Start] --> B{Is test suite available?}
    B -->|Yes| C[Select test suite]
    B -->|No| D[Create new test suite]
    D --> E[Configure test parameters]
    C --> E
    E --> F[Run tests]
    F --> G{Tests passed?}
    G -->|Yes| H[Generate report]
    G -->|No| I[Debug failed tests]
    I --> J[Make code adjustments]
    J --> F
    H --> K[Export results]
    K --> L[End]
```

## Інтеграційна архітектура

Для об'єднання frontend та backend компонентів використовується Tauri framework, що дозволяє створити єдиний десктопний додаток.

```mermaid
graph TD
    subgraph Desktop Application
        subgraph Tauri
            WV[WebView] --> FE[Frontend React App]
            RS[Rust Backend] --> BE[Backend FastAPI]
            WV <--> RS
        end
    end
    
    FE <--> API[API Endpoints]
    BE <--> DB[(MongoDB)]
    
    classDef frontend fill:#d1f0d1,stroke:#333
    classDef backend fill:#d1e0ff,stroke:#333
    classDef tauri fill:#ffe6cc,stroke:#333
    classDef database fill:#e6ccff,stroke:#333
    
    class FE frontend
    class BE,API backend
    class WV,RS tauri
    class DB database
```

## Висновки щодо архітектури

Poly Micro Manager має добре продуману архітектуру з наступними перевагами:

1. **Модульний дизайн**: Чітке розділення обов'язків робить кодову базу високо підтримуваною
2. **Масштабованість**: Stateless дизайн з контейнеризацією та кешуванням забезпечує відмінне масштабування
3. **Тестованість**: Патерн dependency injection та чіткі межі між шарами спрощують тестування
4. **Спостережуваність**: Система включає комплексну систему логування для моніторингу та дебагу
5. **Гнучкість**: Архітектура забезпечує стабільну основу для майбутньої еволюції проекту

Ця архітектура поєднує кращі практики як для backend (мікросервісна архітектура), так і для frontend (компонентний підхід з React), забезпечуючи надійну та масштабовану систему для управління мікросервісами.
