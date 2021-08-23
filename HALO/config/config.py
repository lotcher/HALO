class Config:
    damping_score_threshold = 0.999
    sampling = 2

    @classmethod
    def init(cls, **kwargs):
        for k, v in kwargs.items():
            setattr(cls, k.lower(), v)
