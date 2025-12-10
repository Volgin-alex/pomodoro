from pydantic import BaseModel, Field, model_validator


class Task(BaseModel):
    id: int
    name: str | None = None
    pomodor_cnt: int | None = None
    category_id: int = Field(exclude=True)

    @model_validator(mode="after")
    def check_name_or_pomodoro_cnt_is_none(self):
        if self.name is None and self.pomodor_cnt is None:
            raise ValueError("name is pomodor_cnt be provided")
        return self