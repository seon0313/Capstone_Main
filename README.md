# 2024 서울로봇고등학교 캡스톤 대회 - 중심 팀

### 밸런싱 로봇 메인 코드


***

### 개요

2024 서울로봇고의 캡스톤 대회 중심팀 출품작의 메인 소스코드


![circuit.png](/images/rpi4b.svg)

이 프로젝트는 라즈베리파이 기반으로 개발 되었습니다.

***

### 목차
* [개요](#개요)
* [목차](#목차)
* [팀원 소개](#팀원-소개)
* [라이센스](#라이센스)
* [작동 방식](#작동-방식)
* [사용법](#사용법)
* [사용 부품 리스트](#사용-부품-리스트)
***

### 팀원 소개

| 학년 | 이름 | 역할 |
| :---: | :---: | :--- |
| 2 | 추윤선 | 팀장, 코딩, 설계, 제작  |
| 2 | 백수현 | 설계, 조립, 테스트, 제작 |
| 2 | 하정호 | 코딩, 테스트 |

***

### 라이센스

이 프로젝트의 저작권은 중심팀 일동에게 있습니다.

사용시 누구든지 손쉽게 확인할 수 있는 곳에 저작권자를 표시하십시오.

Apache-2.0 license를 따릅니다.

***

### 작동 방식

이 로봇은 하나의 라즈베리파이에 두개의 ESP32가 접속하여 서로 명령을 주고 받으며 로봇을 제어합니다.

Websocket을 이용하여 서버를 열고 Socket API를 활용하여 생성한 Websocket에 ESP32을 연결합니다.

ESP32는 서버로 메세지를 전송할때 본인의 Type를 포함하여 전송합니다. 이는 서버 측에서 해당 메세지가 어떤 역할을 담당한 ESP32에서 전송되었는지 확인하기 위함입니다.

서버는 메세지의 Type를 확인한 후 해당 Type에 등록된 Event 클래스에 메세지의 명령과 arg를 전달합니다.

Event 클래스에서는 해당 명령에 등록된 함수를 호출하여 명령을 처리한 결과를 리턴합니다. 리턴된 결과는 메세지 형태(JSON)이며 리턴된 값을 받은 후 바로 해당 ESP32로 전송합니다. 

Event 클래스를 이용하여 언제든지 기능을 추가 할 수 있도록 개발하였습니다.

Event 클래스의 하위 클래스를 만든 후 setEvent()
함수를 이용해 서버에 Event를 등록할 수 있습니다.
***

### 사용법

> **이벤트** 클래스 사용법

`HelloWorld` 타입의 이벤트를 만들어 보겠습니다.

```python
from Event import Event
```
우선 이벤트 클래스를 `import`합니다.

```python
class helloWorldEvent(Event):
  def __init__(self):
    super().__init__()
```
`Event`를 상속받는 `helloWorldEvent` 클래스를 선언합니다.

```python
def __init__(self):
  super().__init__()
  self.requests = {'HelloWorld':self.helloWorld}
```
`HelloWorld` 명령을 받았을 경우 호출시킬 함수를 등록합니다.

```python
def helloWorld(self, *args):
  print(f'HelloWorld! Get args: {args})
  return 'Hello Client!'
```
`HelloWorld` 명령을 받은 경우 호출되는 함수를 선언했습니다. `HelloWorld` 명령을 받으면 `"HelloWorld!"`를 출력하고, 받은 args들을 함께 출력합니다.
그 후 `'Hello Client!`를 전송합니다.

메세지를 전송한 클라이언트에게 메세지를 전송할려면 전송할 메세지를 `return`하면 됩니다. 만약 특정 타입의 클라이언트에게 전송할려면 메세지와 타입을 같이 아래와 같이 리턴해 주세요.

```python
return 'HelloWorld', '2th_Arduino' # To. "2th_Arduino"
```

다음은 전체 코드입니다.

```python
class helloWorldEvent(Event):
  def __init__(self):
    super().__init__()
    self.requests = {'HelloWorld':self.helloWorld}
  def helloWorld(self, *args):
    print(f'HelloWorld! Get args: {args})
```

이렇게 이벤트 클래스를 만들었습니다.

그럼 이벤트 클래스를 서버에 등록해 보겠습니다.
```python
# main.py
if __name__ == '__main__':
  from helloWorldEvent import helloWorldEvent
  setEvent('HelloWorld', helloWorldEvent())
```

`HelloWorld` 타입의 클래스를 `helloWorldEvent`로 등록했습니다.

***
### 사용 부품 리스트
| 이름 | 개수  |
| --- |---: |
|라즈베리파이 4B 4GB | 1 |
|3pie Led | 222 |
| Nema17 | 2 |
| 스탭모터 드라이버 | 2 |
| Esp32 | 2 |

***
