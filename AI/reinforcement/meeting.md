아래는 각 시점의 결과를 센서별로 나누어 가독성을 높인 표입니다. 각 센서의 **측정값**, **비트마스크**, **창문 상태** 및 **상태 유지 비트마스크 (hold_mask)**가 표시됩니다.

| 시점 | 센서      | 실내 측정값 | 실내 비트마스크 | 실외 측정값 | 실외 비트마스크 | 창문 상태                | 상태 유지 비트마스크 (hold_mask) |
|------|-----------|-------------|-----------------|-------------|-----------------|--------------------------|----------------------------------|
| 1    | eco2      | 1800        | 0b11            | 550         | 0b0            | 창문 열림 (환기 필요)    | 0b111011                         |
|      | voc       | 500         | 0b1             | 200         | 0b0            |                          |                                  |
|      | pm10      | 150         | 0b11            | 45          | 0b0            |                          |                                  |
|      | pm2.5     | 60          | 0b1             | 25          | 0b0            |                          |                                  |
| 2    | eco2      | 1700        | 0b1             | 540         | 0b0            | 창문 열림 유지 (임계치 초과 중) | 0b111011                 |
|      | voc       | 450         | 0b1             | 180         | 0b0            |                          |                                  |
|      | pm10      | 140         | 0b11            | 50          | 0b0            |                          |                                  |
|      | pm2.5     | 55          | 0b1             | 22          | 0b0            |                          |                                  |
| 3    | eco2      | 1000        | 0b0             | 520         | 0b0            | 창문 닫음 (공기질 양호)   | 0b0                             |
|      | voc       | 300         | 0b0             | 160         | 0b0            |                          |                                  |
|      | pm10      | 70          | 0b0             | 40          | 0b0            |                          |                                  |
|      | pm2.5     | 40          | 0b0             | 20          | 0b0            |                          |                                  |

### 설명
- **시점 1**: `eco2`, `pm10`, `pm2.5` 센서가 임계치를 초과하여 창문이 열리며, `hold_mask`가 설정됩니다.
- **시점 2**: 일부 센서가 정상화되었지만 여전히 `hold_mask`가 설정되어 창문이 열림 상태를 유지합니다.
- **시점 3**: 모든 센서가 정상 범위로 돌아와 `hold_mask`가 해제되고 창문이 닫힙니다.

이 표는 시점별 센서 상태와 창문 상태의 변화를 직관적으로 보여줍니다.