from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from lightapi import EndpointRateLimitMiddleware, HttpMethod, LightApi, RestEndpoint
from lightapi.fields import Field


class BookEndpoint(RestEndpoint, HttpMethod.GET):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)

    class Meta:
        rate_limit = {"requests": 3, "window": 60}


if __name__ == "__main__":
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    app = LightApi(engine=engine, middlewares=[EndpointRateLimitMiddleware])
    app.register({"/books": BookEndpoint})
    app.run(host="0.0.0.0", port=8000, debug=True)
