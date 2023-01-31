from django.db import models


# 질문 Question 클래스 생성 : subject, content, create_date
class Question(models.Model):
    subject = models.CharField(max_length=200)  # 글자수 제한
    content = models.TextField()  # 글자수 제한이 없는 경우
    create_date = models.DateTimeField()  # 날자 + 시간

    def __str__(self):
        return self.subject


class Answer(models.Model):
    # 답변에 연관된 질문이 삭제되면 답변도 모두 삭제하세요.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()  # 글자수 제한이 없는 경우
    create_date = models.DateTimeField()  # 날자 + 시간

    def __str__(self):
        return self.content


