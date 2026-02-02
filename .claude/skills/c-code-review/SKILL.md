# SKILL.md - C/C++ 코드 리뷰 가이드라인

## 🎯 목적
이 문서는 안전하고 효과적인 C/C++ 코드 리뷰를 수행하기 위한 종합 가이드라인을 제공합니다. 특히 메모리 안전성과 보안 취약점에 중점을 둡니다.

---

## 📋 코드 리뷰 체크리스트

### ✅ 메모리 안전성
- [ ] 버퍼 오버플로우 취약점이 없는가
- [ ] 메모리 누수가 없는가 (malloc/free 쌍 확인)
- [ ] Double free 위험이 없는가
- [ ] Use-after-free 취약점이 없는가
- [ ] 널 포인터 역참조가 방지되는가

### ✅ 보안
- [ ] 안전하지 않은 함수 사용이 없는가 (strcpy, gets, sprintf 등)
- [ ] 포맷 스트링 공격 취약점이 없는가
- [ ] 정수 오버플로우가 방지되는가
- [ ] 입력 검증이 적절한가
- [ ] 경계 검사가 수행되는가

### ✅ 코드 품질
- [ ] 함수가 단일 책임을 가지는가
- [ ] 코드가 읽기 쉽고 명확한가
- [ ] 적절한 에러 처리가 되는가
- [ ] 리소스 정리가 확실한가 (RAII 패턴)
- [ ] 코드 중복이 없는가

---

## 🔍 세부 리뷰 영역

### 1. 위험한 문자열 함수 (Critical)

#### ✗ 절대 사용하지 말 것
```c
// ❌ gets() - 버퍼 크기를 확인하지 않음 (C11에서 제거됨)
char buffer[100];
gets(buffer);  // 절대 사용 금지!

// ❌ strcpy() - 대상 버퍼 크기를 확인하지 않음
char dest[10];
strcpy(dest, source);  // 버퍼 오버플로우 위험!

// ❌ strcat() - 대상 버퍼 크기를 확인하지 않음
strcat(dest, source);  // 버퍼 오버플로우 위험!

// ❌ sprintf() - 버퍼 크기를 확인하지 않음
sprintf(buffer, "%s %d", str, num);  // 위험!
```

#### ✓ 안전한 대안 사용
```c
// ✅ fgets() - 버퍼 크기 지정
char buffer[100];
if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
    // 개행 문자 제거
    buffer[strcspn(buffer, "\n")] = '\0';
}

// ✅ strncpy() - 크기 제한 (주의: 널 종료 보장 필요)
char dest[10];
strncpy(dest, source, sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';  // 널 종료 보장

// ✅ strlcpy() - 크기 제한 + 널 종료 보장 (BSD 계열)
#ifdef __BSD__
strlcpy(dest, source, sizeof(dest));
#endif

// ✅ strncat() - 크기 제한
char dest[100] = "Hello ";
strncat(dest, source, sizeof(dest) - strlen(dest) - 1);

// ✅ snprintf() - 버퍼 크기 지정
char buffer[100];
snprintf(buffer, sizeof(buffer), "%s %d", str, num);

// ✅ C11 안전 함수 (선택 사항, 컴파일러 지원 필요)
#ifdef __STDC_LIB_EXT1__
strcpy_s(dest, sizeof(dest), source);
strcat_s(dest, sizeof(dest), source);
sprintf_s(buffer, sizeof(buffer), "%s %d", str, num);
#endif
```

**리뷰 포인트:**
- strcpy, strcat, sprintf, gets 사용 시 즉시 지적
- strncpy 사용 시 널 종료 확인
- 버퍼 크기 계산이 정확한지 확인
- off-by-one 에러 확인

---

### 2. 포맷 스트링 취약점

#### ✗ 위험한 예시
```c
// ❌ 사용자 입력을 포맷 스트링으로 직접 사용
char *user_input = get_user_input();
printf(user_input);  // 공격자가 %x %n 등을 주입 가능!
fprintf(log_file, user_input);  // 위험!
syslog(LOG_INFO, user_input);  // 위험!

// ❌ 동적으로 생성된 포맷 스트링
char format[100];
sprintf(format, "Value: %s", get_format_type());
printf(format);  // 위험!
```

#### ✓ 안전한 예시
```c
// ✅ 포맷 스트링 상수 사용
char *user_input = get_user_input();
printf("%s", user_input);  // 안전
fprintf(log_file, "%s", user_input);  // 안전
syslog(LOG_INFO, "%s", user_input);  // 안전

// ✅ 입력 검증 후 사용
if (validate_input(user_input)) {
    printf("User said: %s\n", user_input);
}

// ✅ fputs 사용 (포맷 스트링 불필요)
fputs(user_input, stdout);
```

**리뷰 포인트:**
- printf/fprintf/syslog 등에 변수를 직접 전달하는지 확인
- 모든 출력 함수에서 포맷 스트링 상수 사용 확인
- 사용자 입력이 포맷 스트링으로 사용되지 않는지 확인

---

### 3. 메모리 관리

#### ✗ 위험한 예시
```c
// ❌ 메모리 누수
void process_data() {
    char *buffer = malloc(1024);
    if (some_error) {
        return;  // 메모리 누수!
    }
    // ... 처리 ...
    free(buffer);
}

// ❌ Double free
char *ptr = malloc(100);
free(ptr);
free(ptr);  // Double free 취약점!

// ❌ Use-after-free
char *ptr = malloc(100);
free(ptr);
strcpy(ptr, "data");  // 해제된 메모리 사용!

// ❌ 널 포인터 역참조
char *ptr = malloc(1024);
strcpy(ptr, source);  // malloc 실패 시 널 포인터 역참조!

// ❌ 스택 버퍼 오버플로우
void vulnerable_function(char *input) {
    char buffer[64];
    strcpy(buffer, input);  // 입력 크기 확인 안 함!
}

// ❌ 힙 버퍼 오버플로우
char *buffer = malloc(64);
strcpy(buffer, long_string);  // 크기 확인 안 함!
```

#### ✓ 안전한 예시
```c
// ✅ RAII 패턴 (리소스 정리 보장)
void process_data() {
    char *buffer = malloc(1024);
    if (buffer == NULL) {
        return;  // 할당 실패 처리
    }

    if (some_error) {
        free(buffer);
        return;  // 메모리 해제 후 반환
    }

    // ... 처리 ...
    free(buffer);
}

// ✅ 또는 goto를 사용한 정리 패턴 (Linux 커널 스타일)
void process_data() {
    char *buffer = NULL;
    int ret = 0;

    buffer = malloc(1024);
    if (buffer == NULL) {
        ret = -ENOMEM;
        goto cleanup;
    }

    if (some_error) {
        ret = -EINVAL;
        goto cleanup;
    }

    // ... 처리 ...

cleanup:
    free(buffer);  // NULL 체크 불필요 (free(NULL)은 안전)
    return ret;
}

// ✅ Double free 방지
char *ptr = malloc(100);
if (ptr != NULL) {
    free(ptr);
    ptr = NULL;  // 해제 후 NULL로 설정
}
// 다시 해제해도 안전
free(ptr);  // free(NULL)은 아무 작업도 하지 않음

// ✅ 널 포인터 체크
char *ptr = malloc(1024);
if (ptr == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    return -1;
}
strncpy(ptr, source, 1023);
ptr[1023] = '\0';
free(ptr);

// ✅ 스택 버퍼 안전하게 사용
void safe_function(const char *input) {
    char buffer[64];
    size_t input_len = strlen(input);

    // 입력 크기 검증
    if (input_len >= sizeof(buffer)) {
        fprintf(stderr, "Input too long\n");
        return;
    }

    strncpy(buffer, input, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';
}

// ✅ 힙 버퍼 안전하게 사용
size_t needed_size = strlen(long_string) + 1;
char *buffer = malloc(needed_size);
if (buffer == NULL) {
    return -1;
}
memcpy(buffer, long_string, needed_size);
free(buffer);
```

**리뷰 포인트:**
- 모든 malloc/calloc/realloc에 대응하는 free가 있는지 확인
- 에러 경로에서도 메모리가 해제되는지 확인
- 해제 후 포인터를 NULL로 설정하는지 확인
- malloc 반환값을 항상 확인하는지 체크
- 버퍼 크기를 올바르게 계산하는지 확인

---

### 4. 정수 오버플로우

#### ✗ 위험한 예시
```c
// ❌ 정수 오버플로우
size_t size = get_user_size();
char *buffer = malloc(size);  // size가 0 또는 매우 큰 값이면?

// ❌ 곱셈 오버플로우
int num_items = get_count();
int item_size = sizeof(struct item);
void *items = malloc(num_items * item_size);  // 오버플로우 가능!

// ❌ 부호 있는 정수 오버플로우
int a = INT_MAX;
int b = a + 1;  // 정의되지 않은 동작!

// ❌ 음수를 크기로 사용
int user_size = get_input();  // -1이 입력되면?
char *buffer = malloc(user_size);  // 큰 양수로 변환됨!
```

#### ✓ 안전한 예시
```c
// ✅ 입력 검증
size_t size = get_user_size();
if (size == 0 || size > MAX_ALLOWED_SIZE) {
    fprintf(stderr, "Invalid size\n");
    return -1;
}
char *buffer = malloc(size);

// ✅ 곱셈 오버플로우 체크
#include <stdint.h>
#include <limits.h>

bool safe_multiply(size_t a, size_t b, size_t *result) {
    if (a > 0 && b > SIZE_MAX / a) {
        return false;  // 오버플로우 발생
    }
    *result = a * b;
    return true;
}

size_t num_items = get_count();
size_t item_size = sizeof(struct item);
size_t total_size;

if (!safe_multiply(num_items, item_size, &total_size)) {
    fprintf(stderr, "Size calculation overflow\n");
    return -1;
}

void *items = malloc(total_size);

// ✅ C23 calloc 사용 (자동 오버플로우 체크)
void *items = calloc(num_items, item_size);  // 안전

// ✅ 부호 있는 정수 오버플로우 체크
int a = INT_MAX;
if (a > INT_MAX - 1) {
    fprintf(stderr, "Integer overflow\n");
    return -1;
}
int b = a + 1;

// ✅ 크기 검증 (음수 방지)
int user_size = get_input();
if (user_size <= 0 || user_size > MAX_SIZE) {
    fprintf(stderr, "Invalid size\n");
    return -1;
}
char *buffer = malloc((size_t)user_size);
```

**리뷰 포인트:**
- 산술 연산 전에 오버플로우 체크
- 사용자 입력을 크기로 사용할 때 검증
- calloc 사용 권장 (오버플로우 체크 내장)
- 부호 있는/없는 정수 변환 시 주의

---

### 5. 배열 경계 검사

#### ✗ 위험한 예시
```c
// ❌ 배열 경계 초과
int arr[10];
for (int i = 0; i <= 10; i++) {  // off-by-one 에러!
    arr[i] = i;
}

// ❌ 사용자 입력으로 인덱스 사용
int index = get_user_index();
int value = array[index];  // 범위 검증 없음!

// ❌ 문자열 버퍼 오버플로우
char buffer[10];
for (int i = 0; i < 20; i++) {
    buffer[i] = 'A';  // 버퍼 범위 초과!
}
```

#### ✓ 안전한 예시
```c
// ✅ 올바른 배열 반복
int arr[10];
for (int i = 0; i < 10; i++) {  // < 사용
    arr[i] = i;
}

// 또는
for (size_t i = 0; i < sizeof(arr) / sizeof(arr[0]); i++) {
    arr[i] = i;
}

// ✅ 인덱스 검증
int index = get_user_index();
if (index < 0 || index >= array_size) {
    fprintf(stderr, "Index out of bounds\n");
    return -1;
}
int value = array[index];

// ✅ 버퍼 크기 확인
char buffer[10];
size_t buffer_size = sizeof(buffer);
for (size_t i = 0; i < buffer_size && i < 20; i++) {
    buffer[i] = 'A';
}

// ✅ 매크로 사용
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]))

int arr[10];
for (size_t i = 0; i < ARRAY_SIZE(arr); i++) {
    arr[i] = i;
}
```

**리뷰 포인트:**
- 루프 조건에서 off-by-one 에러 확인 (<=, <)
- 배열 인덱스 사용 전 범위 검증
- sizeof를 사용한 배열 크기 계산
- 매직 넘버 대신 상수 사용

---

### 6. 파일 및 리소스 관리

#### ✗ 위험한 예시
```c
// ❌ 파일 핸들 누수
FILE *fp = fopen("data.txt", "r");
if (some_error) {
    return;  // 파일 닫지 않음!
}
fclose(fp);

// ❌ 널 포인터 체크 없음
FILE *fp = fopen("data.txt", "r");
fread(buffer, 1, size, fp);  // fopen 실패 시 크래시!
fclose(fp);

// ❌ TOCTOU (Time-of-check to time-of-use) 취약점
if (access("file.txt", W_OK) == 0) {
    // 경쟁 조건: 다른 프로세스가 파일 권한 변경 가능
    FILE *fp = fopen("file.txt", "w");
}
```

#### ✓ 안전한 예시
```c
// ✅ 파일 핸들 안전하게 관리
FILE *fp = fopen("data.txt", "r");
if (fp == NULL) {
    perror("fopen failed");
    return -1;
}

// 에러 처리 경로에서도 fclose 호출
if (some_error) {
    fclose(fp);
    return -1;
}

// 정상 경로
// ... 처리 ...
fclose(fp);

// ✅ goto를 사용한 리소스 정리 패턴
int process_file(const char *filename) {
    FILE *fp = NULL;
    char *buffer = NULL;
    int ret = 0;

    fp = fopen(filename, "r");
    if (fp == NULL) {
        perror("fopen failed");
        ret = -1;
        goto cleanup;
    }

    buffer = malloc(BUFFER_SIZE);
    if (buffer == NULL) {
        ret = -1;
        goto cleanup;
    }

    // ... 처리 ...

cleanup:
    if (fp != NULL) {
        fclose(fp);
    }
    free(buffer);  // free(NULL)은 안전
    return ret;
}

// ✅ TOCTOU 방지 - 직접 열기 시도
FILE *fp = fopen("file.txt", "w");
if (fp == NULL) {
    if (errno == EACCES) {
        fprintf(stderr, "Permission denied\n");
    }
    return -1;
}
// 파일 사용
fclose(fp);
```

**리뷰 포인트:**
- 모든 fopen에 대응하는 fclose 확인
- 파일 포인터 널 체크
- 에러 경로에서 리소스 정리
- TOCTOU 취약점 확인

---

## 🚨 공통 취약점 패턴

### 1. 경쟁 조건 (Race Condition)
```c
// ❌ 위험
if (file_exists("temp.txt")) {
    fp = fopen("temp.txt", "w");  // 다른 프로세스가 파일 변경 가능
}

// ✅ 안전
fp = fopen("temp.txt", "wx");  // 독점 생성 모드
```

### 2. 시그널 핸들러 안전성
```c
// ❌ 위험 - async-signal-unsafe 함수 호출
void signal_handler(int sig) {
    printf("Signal received\n");  // printf는 unsafe!
    malloc(100);  // malloc도 unsafe!
}

// ✅ 안전 - async-signal-safe 함수만 사용
volatile sig_atomic_t signal_received = 0;

void signal_handler(int sig) {
    signal_received = 1;  // 간단한 플래그만 설정
}

int main() {
    signal(SIGINT, signal_handler);
    while (!signal_received) {
        // 메인 루프에서 플래그 확인
    }
}
```

### 3. 포인터 별칭 (Pointer Aliasing)
```c
// ❌ 위험 - restrict 키워드 없이 중첩 가능
void copy_data(int *dest, int *src, size_t n) {
    for (size_t i = 0; i < n; i++) {
        dest[i] = src[i];  // dest와 src가 겹칠 수 있음
    }
}

// ✅ 안전 - restrict 키워드 사용
void copy_data(int * restrict dest, const int * restrict src, size_t n) {
    for (size_t i = 0; i < n; i++) {
        dest[i] = src[i];
    }
}

// 또는 memmove 사용 (겹침 허용)
memmove(dest, src, n * sizeof(int));
```

---

## 🔧 도구 활용

### 정적 분석 도구
```bash
# Clang Static Analyzer
clang --analyze src/*.c

# Cppcheck
cppcheck --enable=all src/

# Flawfinder (보안 취약점 검사)
flawfinder src/

# Splint (보안 및 스타일 검사)
splint +posixlib src/*.c

# GCC 경고 옵션 최대화
gcc -Wall -Wextra -Werror -Wformat-security \
    -Wstrict-overflow -fstack-protector-strong \
    -D_FORTIFY_SOURCE=2 src/*.c
```

### 동적 분석 도구
```bash
# Valgrind (메모리 누수 검사)
valgrind --leak-check=full --show-leak-kinds=all ./program

# AddressSanitizer (메모리 오류 검사)
gcc -fsanitize=address -g src/*.c -o program
./program

# UndefinedBehaviorSanitizer
gcc -fsanitize=undefined -g src/*.c -o program
./program

# ThreadSanitizer (데이터 경쟁 검사)
gcc -fsanitize=thread -g src/*.c -o program
./program
```

---

## 📊 코드 리뷰 우선순위

### 🔴 Critical (즉시 수정 필수)
- gets, strcpy, strcat, sprintf 사용
- 포맷 스트링 취약점
- 버퍼 오버플로우
- Use-after-free
- Double free
- 널 포인터 역참조

### 🟡 High (수정 강력 권장)
- strncpy 후 널 종료 누락
- 메모리 누수
- 정수 오버플로우
- 입력 검증 누락
- 리소스 누수 (파일 핸들 등)

### 🟢 Medium (수정 권장)
- 불필요한 malloc/free
- 비효율적인 알고리즘
- 코드 중복
- 명명 규칙 위반

---

## 💬 리뷰 코멘트 작성 예시

### ✓ 좋은 코멘트
```
"strcpy()는 버퍼 오버플로우에 취약합니다.
strncpy()를 사용하고 널 종료를 보장하세요:

strncpy(dest, src, sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';

또는 더 나은 방법으로 snprintf()를 사용할 수 있습니다:
snprintf(dest, sizeof(dest), "%s", src);
"
```

---

## 📝 안전한 코딩 체크리스트

- [ ] 모든 문자열 함수가 안전한 버전인가 (strncpy, snprintf 등)
- [ ] 모든 버퍼 접근에 경계 검사가 있는가
- [ ] 모든 포인터가 사용 전에 널 체크되는가
- [ ] 모든 malloc에 대응하는 free가 있는가
- [ ] 모든 파일이 닫히는가 (에러 경로 포함)
- [ ] 사용자 입력이 검증되는가
- [ ] 정수 오버플로우가 방지되는가
- [ ] 포맷 스트링이 상수인가
- [ ] 컴파일러 경고가 모두 해결되었는가 (-Wall -Wextra)
- [ ] AddressSanitizer로 테스트했는가

---

## 🎓 학습 자료

### 보안 가이드
- [CERT C Coding Standard](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard)
- [CWE Top 25 Most Dangerous Software Weaknesses](https://cwe.mitre.org/top25/)
- [OWASP C-Based Toolchain Hardening](https://owasp.org/www-community/vulnerabilities/C-Based_Toolchain_Hardening)

### 도서
- "The Art of Software Security Assessment" - Mark Dowd
- "Secure Coding in C and C++" - Robert C. Seacord
- "Writing Secure Code" - Michael Howard

---

## 📅 유지보수

**최종 업데이트**: 2026-02-02
**검토 주기**: 분기별
**담당자**: Security Team

### 변경 이력
- v1.0 - C/C++ 보안 중심 코드 리뷰 가이드라인 초기 작성
