from dataclasses import dataclass

@dataclass
class STTConfig:
	engine: str
	api_key: str

@dataclass
class TTSConfig:
	engine: str
	api_key: str

@dataclass
class LLMConfig:
	engine: str
	api_key: str
	system_prompt: str

@dataclass
class BotConfig:
	stt: STTConfig
	tts: TTSConfig
	llm: LLMConfig

def setup_bot(stt_config: STTConfig, tts_config: TTSConfig, llm_config: LLMConfig) -> BotConfig:
	return BotConfig(stt=stt_config, tts=tts_config, llm=llm_config)