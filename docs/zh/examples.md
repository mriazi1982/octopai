# 示例

这里是使用 EXO 进行各种任务的实际示例。

## 示例 1：URL 到 Markdown 转换

### 基本转换

```python
from exo import EXO

exo = EXO()

# 转换网页
content = exo.convert_url("https://example.com")

# 保存到文件
with open("output.md", "w") as f:
    f.write(content)
```

### 使用爬虫

```python
from exo import convert

# 转换并下载所有资源
content = convert("https://example.com", use_crawler=True)
print("页面已转换，资源已下载！")
```

### CLI 版本

```bash
exo convert https://example.com -o page.md --crawler
```

## 示例 2：创建技能

### 数据处理技能

```python
from exo import create

skill = create(
    """
    一个从文件读取 JSON 数据、
    提取特定字段并生成摘要报告的技能。
    
    要求：
    - 高效处理大 JSON 文件
    - 支持多种输出格式（文本、CSV）
    - 包含对无效 JSON 的错误处理
    """
)

print(skill)
```

### 带资源的技能创建

```python
from exo import EXO

exo = EXO()

# 使用文件作为资源创建技能
skill = exo.create_skill(
    "根据这些数据文件创建数据分析技能",
    name="data-analyzer",
    resources=[
        "data/sample.csv",
        "docs/reference.pdf",
        "images/chart.png"
    ]
)

# 保存到文件
with open("skills/data_analyzer.py", "w") as f:
    f.write(skill)
```

## 示例 3：解析文件资源

### 解析单个文件

```python
from exo import parse

# 解析 PDF 文件
resource = parse("document.pdf")

print(f"类型: {resource.resource_type}")
print(f"页数: {resource.metadata.get('num_pages', 'unknown')}")
print(f"内容预览: {resource.text_content[:200]}...")
```

### 解析多个文件

```python
from exo import EXO

exo = EXO()

files = [
    "data/data.csv",
    "docs/manual.docx",
    "images/diagram.png",
    "video/tutorial.mp4"
]

# 解析所有文件
resources = exo.parse_multiple_files(files)

# 转换为技能资源格式
for resource in resources:
    skill_resource = resource.to_skill_resource()
    print(f"\n=== {os.path.basename(resource.file_path)} ===")
    print(skill_resource[:300] + "...")
```

### 直接转换为技能资源

```python
from exo import parse_to_skill_resource

# 一步解析并转换
skill_resource = parse_to_skill_resource("data.xlsx")

# 在技能创建中使用
from exo import create

skill = create(
    f"创建一个使用此数据的技能：\n{skill_resource}",
    name="excel-processor"
)
```

## 示例 4：进化技能

### 简单进化

```python
from exo import evolve

# 改进现有技能
evolved_skill = evolve(
    "skills/my-skill.py",
    "添加日志记录以跟踪技能在做什么"
)

# 保存改进版本
with open("skills/my-skill-improved.py", "w") as f:
    f.write(evolved_skill)
```

### 使用引擎的多次迭代

```python
from exo import EXO

exo = EXO()

# 使用高级进化引擎获得更好的结果
final_skill = exo.evolve_skill(
    "skills/data-processor.py",
    "针对大数据集优化速度和内存效率",
    use_engine=True,
    iterations=5
)
```

## 示例 5：直接使用进化引擎

```python
from exo.core.evolution_engine import EvolutionEngine

# 创建引擎
engine = EvolutionEngine(
    model="openai/gpt-5.4",
    max_iterations=5
)

# 定义初始候选
initial_skill = """
def process_data(data):
    return [x * 2 for x in data]
"""

# 定义评估任务
tasks = [
    {"input": [1, 2, 3], "expected": [2, 4, 6]},
    {"input": [0, -1, 5], "expected": [0, -2, 10]}
]

# 定义评估器
def evaluator(candidate, task):
    # 执行候选代码并评估
    # 这是一个简化示例
    try:
        exec(candidate, globals())
        result = process_data(task["input"])
        score = 1.0 if result == task["expected"] else 0.0
        return score, f"结果: {result}"
    except Exception as e:
        return 0.0, f"错误: {str(e)}"

# 运行进化
result = engine.evolve(
    initial_candidate=initial_skill,
    tasks=tasks,
    evaluator=evaluator
)

print(f"最佳技能:\n{result.best_candidate}")
print(f"最佳分数: {result.best_score}")
```

## 示例 6：完整工作流

```python
from exo import EXO
import os

def main():
    # 初始化 EXO
    exo = EXO(model="openai/gpt-5.4")
    
    # 步骤 1：解析资源文件
    print("解析资源文件...")
    resources = []
    
    data_files = [
        "data/sample.csv",
        "docs/api-reference.pdf",
        "examples/demo.py"
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            resource = exo.parse_file(file_path)
            resources.append(resource)
            print(f"  已解析: {file_path}")
    
    # 步骤 2：使用资源创建技能
    print("\n创建技能...")
    skill = exo.create_skill(
        "创建一个处理数据文件的综合技能",
        name="data-processor",
        resources=[r.file_path for r in resources]
    )
    
    with open("skills/data_processor.py", "w") as f:
        f.write(skill)
    
    # 步骤 3：进化和改进技能
    print("\n进化技能...")
    final_skill = exo.evolve_skill(
        "skills/data_processor.py",
        "添加速率限制、重试和全面的错误处理",
        iterations=3
    )
    
    with open("skills/data_processor_final.py", "w") as f:
        f.write(final_skill)
    
    print("\n工作流完成！")

if __name__ == "__main__":
    main()
```

## 示例 7：批处理

```python
from exo import parse, parse_to_skill_resource
import os

# 要处理的文件目录
input_dir = "./documents"
output_dir = "./resources"

os.makedirs(output_dir, exist_ok=True)

# 处理目录中的所有文件
for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    
    if os.path.isfile(file_path):
        print(f"处理 {filename}...")
        
        try:
            # 解析并转换为技能资源
            skill_resource = parse_to_skill_resource(file_path)
            
            # 保存输出
            output_path = os.path.join(output_dir, f"{filename}.md")
            with open(output_path, "w") as f:
                f.write(skill_resource)
            
            print(f"  已保存到 {output_path}")
            
        except Exception as e:
            print(f"  错误: {str(e)}")

print("所有文件已处理！")
```

## 示例 8：与其他工具集成

```python
from exo import EXO
import git
import os

exo = EXO()

def process_repo_docs(repo_url, local_path):
    # 克隆仓库
    if not os.path.exists(local_path):
        git.Repo.clone_from(repo_url, local_path)
    
    # 查找并解析文档
    docs_dir = os.path.join(local_path, "docs")
    
    if os.path.exists(docs_dir):
        parsed_resources = []
        
        # 解析所有文档文件
        for filename in os.listdir(docs_dir):
            file_path = os.path.join(docs_dir, filename)
            if os.path.isfile(file_path):
                try:
                    resource = exo.parse_file(file_path)
                    parsed_resources.append(resource)
                    print(f"已解析: {filename}")
                except Exception as e:
                    print(f"跳过 {filename}: {str(e)}")
        
        # 基于文档创建技能
        if parsed_resources:
            skill = exo.create_skill(
                "创建一个演示如何使用此项目的技能",
                name="project-demo",
                resources=[r.file_path for r in parsed_resources[:3]]  # 使用前 3 个资源
            )
            
            skill_path = os.path.join(local_path, "exo_skill.py")
            with open(skill_path, "w") as f:
                f.write(skill)
            
            print(f"\n技能已创建在: {skill_path}")

# 使用
process_repo_docs(
    "https://github.com/example/project.git",
    "./temp-project"
)
```
