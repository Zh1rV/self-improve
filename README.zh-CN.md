# self-improve

[English README](./README.md)

`self-improve` 是一个用于在仓库中执行有边界、带验证门槛的持续改进循环的 Codex skill。

它要解决的是自动化编码工作流中的一个常见问题：模型也许能发现值得修的地方，但如果没有明确护栏，就容易漂移、改太多、跳过验证，或者做出很难复查的改动。

这个 skill 把流程控制得尽量简单、透明：

1. 建立基线并识别候选改进项。
2. 对候选项打分，选择高价值、低风险目标。
3. 只做最小且安全的改动。
4. 在继续前验证结果。
5. 重复小步迭代，直到预算用完或没有安全目标为止。

## 核心流程

当前版本采用单智能体的迭代循环，而不是多智能体系统。

- 它更偏向短而重复的推理循环，而不是一次特别长的思维链。
- 每一轮都应产出一个边界清晰的改动，并附带明确的验证证据。
- 这个 skill 优先强调可观测性与可控性，而不是“放手全自动”。

也就是说，它的循环是：

`baseline -> select target -> patch -> validate -> log -> continue or stop`

## 安装方法

从仓库根目录将这个 skill 安装到 Codex：

1. 在 Codex 中输入，让它从 GitHub 安装这个 skill：
   `Use skill-installer to install this skill from GitHub: https://github.com/Zh1rV/self-improve.git`
2. 安装完成后重启 Codex，以便加载这个新 skill。

安装后的 skill 名称：

- `self-improve`

## 仓库内容

- [`SKILL.md`](./SKILL.md)：skill 主定义与运行契约
- [`agents/openai.yaml`](./agents/openai.yaml)：面向 agent 的元数据
- [`references/`](./references)：打分、验证顺序、checkpoint、回滚、循环控制等参考文档
- [`scripts/`](./scripts)：日志、checkpoint 生成、候选排序、验证与无人值守循环执行脚本

## 典型使用场景

当你希望 Codex 持续改进一个代码库，但又希望所有改动都保持“小步、可审查、带验证”的特征时，就适合使用这个 skill。
